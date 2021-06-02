from fractions import Fraction
from liborderbook.orderbook_helper import RtOrderbookWriter
import random
import sys
from pprint import pprint
import ccxt
import json
from pprint import pprint
import time
#from db_inquirer import DatabaseQuerier
from local_models import Service, Instrument
import signal
import os
import universal_listenner
import threading
from slack_lib import send_slack_alert
from decimal import Decimal

def dec(n, d):
	return Decimal(n) / Decimal(d)


class OrderbookFeeder(object):
    def __init__(self, stream_port, shm, exchange, ccxt_instrument):
        self.writer = RtOrderbookWriter(shm)
        self.shm = shm
        self.restart_listenning()
        self.circle_counter = 0
        self.exchange = exchange
        self.ccxt_instrument = ccxt_instrument
        exchange_class = getattr(ccxt, exchange.lower())
        self.rest_client = exchange_class()
        self.lock = threading.Lock()
        self.insert_thread = threading.Thread(target=self.process_queue)
        self.insert_thread.start()
        time.sleep(2)
        print("Requested start of process queue thread")
        self.lstr = universal_listenner.UniversalFeedListenner('127.0.0.1', stream_port, exchange, 'orderbook', on_receive=self.queue_update)
        print(f"Starting up Feed Listenner for {exchange} listenning to stream port {stream_port} writing to {shm}")
    
    def run(self):
        self.listen_thread = threading.Thread(target=self.lstr.run)
        self.listen_thread.start()

    def stop(self):
        self.lstr.stop()

    def restart_listenning(self):
        print("Restarting listenning...")
        self.starting = True
        self.queue = []
        self.start_time = time.time()

    def queue_update(self, update):
        self.lock.acquire()
        try:
            if update['server_received'] == -1:
                self.restart_listenning()
            self.queue.append(update)
            if self.starting:
                if len(self.queue) > 2:
                    initial_book = self.fetch_orderbook_from_rest()
                    self.queue = [initial_book] + self.queue
                    self.starting = False
                    print("Enough cached data, inserting.")
            if 'sequenceId' in update and update['sequenceId'] > 0:
                self.queue.sort(key=lambda x: x['sequenceId'])
            else:
                self.queue.sort(key=lambda x: x['server_received'])
        except Exception as e:
            print(f"Failed to update queue ({e}) with:")
            pprint(update)
        finally:
            self.lock.release()

    def fetch_orderbook_from_rest(self):
        print("Fetching full orderbook from REST interface", self.ccxt_instrument.name)
        raw_ob = self.rest_client.fetch_l2_order_book(self.ccxt_instrument.name)
        raw_ob['server_received'] = self.rest_client.milliseconds()
        raw_ob['sequenceId'] = 0
        return raw_ob

    def process_queue(self):
        print("Starting process queue thread")
        while True:
            if self.starting:
                print("Ignoring queue as starting...")
                time.sleep(0.5)
                continue
            if len(self.queue) == 0:
                continue
            self.lock.acquire()
            update = self.queue.pop(0)
            #print("Processing update in queue:", update)
            self.lock.release()
            self.display_insert(update)

    def display_insert(self, update):
        bids, asks = update['bids'], update['asks']
        if 'Binance' == self.exchange or update.get('sequenceId') == 0:
            print(f'Resetting content of Orderbook')
            self.writer.reset_content()
            print(f'Finished resetting content of Orderbook')
        if self.circle_counter > 400:
            print("Cleaning first entries of orderbook", dec(*self.writer.first_price(True)), dec(*self.writer.first_price(False)))
            self.writer.clean_top_bid()
            self.writer.clean_top_ask()
            self.circle_counter = 0
        if len(bids) > 1:
            quantities = [str(bid[1]) for bid in bids] if update.get('sequenceId') == 0 else [bid['size'] for bid in bids]
            prices = [str(bid[0]) for bid in bids] if update.get('sequenceId') == 0 else [bid['price'] for bid in bids]
            self.writer.set_bid_quantities_at(quantities, prices)
            self.circle_counter += len(bids)
        else:
            for bid in bids:
                if update.get('sequenceId') == 0:
                    print("Inserting in {} REST bid: {}@{}".format(self.shm, str(bid[1]), str(bid[0])))
                    self.writer.set_bid_quantity_at(str(bid[1]), str(bid[0]))
                else:
                    #print("Inserting {} in {} bid from {}: {}@{}".format(self.circle_counter, self.shm, update['exchange'], bid['size'], bid['price']))
                    self.writer.set_bid_quantity_at(bid['size'], bid['price'])
                self.circle_counter += 1
        if len(asks) > 1:
            quantities = [str(ask[1]) for ask in asks] if update.get('sequenceId') == 0 else [ask['size'] for ask in asks]
            prices = [str(ask[0]) for ask in asks] if update.get('sequenceId') == 0 else [ask['price'] for ask in asks]
            self.writer.set_ask_quantities_at(quantities, prices)
            self.circle_counter += len(asks)
        else:
            for ask in asks:
                if update.get('sequenceId') == 0:
                    print("Inserting in {} REST ask: {}@{}".format(self.shm, str(ask[1]), str(ask[0])))
                    self.writer.set_ask_quantity_at(str(ask[1]), str(ask[0]))
                else:
                    #print("Inserting {} in {} ask from {}: {}@{}".format(self.circle_counter, self.shm, update['exchange'], ask['size'], ask['price']))
                    self.writer.set_ask_quantity_at(ask['size'], ask['price'])
                self.circle_counter += 1

        if not self.writer.is_sound() and (time.time() - self.start_time) > 4 :
            message = '[FEEDER] Incoherent ORDERBOOK: crossing detected, resetting' + self.shm
            print(message)
            send_slack_alert("#alerts", message)
            pprint(self.writer.snapshot_bids(10))
            pprint(self.writer.snapshot_asks(10))
            self.lock.acquire()
            self.restart_listenning()
            self.lock.release()
            self.writer.reset_content() 
        
        


    def reset_orderbook(self):
        self.writer.reset_content()


def launch_feeder(stream_port, shm_name, exchange, ccxt_instrument):
    print("Launching orderbook feeder for", exchange, ccxt_instrument.name, "listenning on port", stream_port)
    feeder = OrderbookFeeder(stream_port, shm_name, exchange, ccxt_instrument)

    def term_signal_handler(sig, frame):
        feeder.stop()
        print("Stopping feeder")
        print("Releasing lock if needed...")
        if feeder.lock.locked():
            feeder.lock.release()

    signal.signal(signal.SIGTERM, term_signal_handler)


    feeder.run()
    feeder.insert_thread.join()

if __name__ == "__main__":
    print("Starting orderbook feeder process")
    #db_service_interface = DatabaseQuerier('127.0.0.1', 5678)
    exchange_name, instrument_name = sys.argv[1], sys.argv[2]

    stream = Service.get((Service.name == 'OrderbookDataStream') & (Service.exchange == exchange_name) & (Service.instrument == instrument_name))
    #stream = db_service_interface.find_service('OrderbookDataStream', instrument=instrument_name, exchange=exchange_name)
    
    exchange_instrument = Instrument.get((Instrument.exchange_name == exchange_name) & (Instrument.name == instrument_name))
    #exchange_instrument = db_service_interface.find_instrument(instrument_name, exchange_name)

    ccxt_instrument = Instrument.get((Instrument.exchange_name == 'ccxt') & (Instrument.base == exchange_instrument.base) & (Instrument.quote == exchange_instrument.quote) & (Instrument.kind == exchange_instrument.kind))
    #ccxt_instrument = db_service_interface.find_ccxt_instrument(exchange_name, instrument_name)

    shm_name = f"/shm_{exchange_name}_" + '%08x' % random.randrange(16**8)

    query = Service.update(address=shm_name).where((Service.name == 'OrderbookFeeder') & (Service.instrument == instrument_name) & (Service.exchange == exchange_name))
    query.execute()

    print("Updated feeder service for", exchange_name, instrument_name, "at", shm_name)
    #db_service_interface.update_service_address(shm_name, 'OrderbookFeeder', exchange_name, instrument_name)

    launch_feeder(stream.port, shm_name, exchange_name, ccxt_instrument)
    