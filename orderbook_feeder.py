from fractions import Fraction
from liborderbook.orderbook_helper import RtOrderbookWriter
import random
import sys
from pprint import pprint
import ccxt
import json
from pprint import pprint
import time
import signal
from models import Service
import os
import universal_listenner
import threading


class OrderbookFeeder(object):
    def __init__(self, stream_port, shm, exchange, market):
        self.writer = RtOrderbookWriter(shm)
        self.shm = shm
        self.starting = True
        self.queue = []
        self.exchange = exchange
        exchange_class = getattr(ccxt, exchange.lower())
        self.rest_client = exchange_class()
        self.lock = threading.Lock()
        self.insert_thread = threading.Thread(target=self.process_queue)
        self.insert_thread.start()
        time.sleep(2)
        print("Requested start of process queue thread")
        self.lstr = universal_listenner.UniversalFeedListenner('127.0.0.1', stream_port, exchange, 'orderbook', on_receive=self.queue_update)
        print(f"Starting up Feed Listenner for {exchange} {stream_port} {shm}")
    
    def run(self):
        self.listen_thread = threading.Thread(target=self.lstr.run)
        self.listen_thread.start()

    def stop(self):
        self.lstr.stop()

    def queue_update(self, update):
        self.lock.acquire()
        try:
            if update['server_received'] == -1:
                self.starting = True
                self.queue = []
            self.queue.append(update)
            if self.starting:
                if len(self.queue) > 2:
                    initial_book = self.fetch_orderbook_from_rest()
                    self.queue = [initial_book] + self.queue
                    self.starting = False
                    print("Enough cached data, inserting...")
            self.queue.sort(key=lambda x: x['sequenceId'])
        finally:
            self.lock.release()

    def fetch_orderbook_from_rest(self):
        raw_ob = self.rest_client.fetch_l2_order_book('BTC/USD')
        raw_ob['sequenceId'] = 0
        return raw_ob

    def process_queue(self):
        print("Starting process queue thread")
        while True:
            if self.starting:
                print("Ignoring queue as starting...")
                time.sleep(1)
                continue
            if len(self.queue) == 0:
                continue
            print("Acquiring lock of queue...")
            self.lock.acquire()
            print("Done Acquiring lock of queue...")
            update = self.queue.pop(0)
            #print("Processing update in queue:", update)
            self.lock.release()
            self.display_insert(update)

    def display_insert(self, update):
        bids, asks = update['bids'], update['asks']
        if 'Binance' == self.exchange or update['sequenceId'] == 0:
            print(f'Resetting content of Orderbook')
            self.writer.reset_content()
            print(f'Finished resetting content of Orderbook')
        for bid in bids:
            if update['sequenceId'] == 0:
                print("Inserting in {} REST bid: {}@{}".format(self.shm, str(bid[1]), str(bid[0])))
                self.writer.set_bid_quantity_at(str(bid[1]), str(bid[0]))
            else:
                print("Inserting in {} bid from {}: {}@{}".format(self.shm, update['exchange'], bid['size'], bid['price']))
                self.writer.set_bid_quantity_at(bid['size'], bid['price'])
        for ask in asks:
            if update['sequenceId'] == 0:
                print("Inserting in {} REST ask: {}@{}".format(self.shm, str(ask[1]), str(ask[0])))
                self.writer.set_ask_quantity_at(str(ask[1]), str(ask[0]))
            else:
                print("Inserting in {} ask from {}: {}@{}".format(self.shm, update['exchange'], ask['size'], ask['price']))
                self.writer.set_ask_quantity_at(ask['size'], ask['price'])

        if not self.writer.is_sound() :
            print('Incoherent ORDERBOOK: crossing detected, resetting')
            pprint(self.writer.snapshot_bids(10))
            pprint(self.writer.snapshot_asks(10))
            self.writer.reset_content()


    def reset_orderbook(self):
        self.writer.reset_content()


def launch_feeder(stream_port, shm_name, exchange, market):
    feeder = OrderbookFeeder(stream_port, shm_name, exchange, market)
    print("Launching orderbook feeder for", exchange, market)

    def term_signal_handler(sig, frame):
        print("Stopping feeder")
        feeder.stop()
        print("Releasing lock if needed...")
        if feeder.lock.locked():
            feeder.lock.release()

    signal.signal(signal.SIGTERM, term_signal_handler)


    feeder.run()
    feeder.insert_thread.join()

if __name__ == "__main__":
    print("Starting orderbook feeder process")
    exchange, market = sys.argv[1], sys.argv[2]
    stream = Service.get((Service.exchange == exchange) & (Service.instrument == market))
    shm_name = f"/shm_{exchange}_" + '%08x' % random.randrange(16**8)

    query = Service.update(address=shm_name).where((Service.name == 'OrderbookFeeder') & (Service.instrument == market) & (Service.exchange == exchange))
    query.execute()
    launch_feeder(stream.port, shm_name, exchange, market)