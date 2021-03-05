from fractions import Fraction
from liborderbook.orderbook_helper import RtOrderbookWriter
import random
import sys
from pprint import pprint
import json
import time
import signal
from models import Service
import os
import universal_listenner
import threading


class OrderbookFeeder(object):
    def __init__(self, stream_port, shm, exchange):
        self.writer = RtOrderbookWriter(shm)
        self.shm = shm
        self.queue = []
        self.exchange = exchange
        self.lock = threading.Lock()
        self.lstr = universal_listenner.UniversalFeedListenner('127.0.0.1', stream_port, exchange, 'orderbook', on_receive=self.display_insert)
        print(f"Starting up Feed Listenner for {exchange} {stream_port} {shm}")
    
    def run(self):
        return self.lstr.run()

    def stop(self):
        self.lstr.stop()

    def queue_update(self, update):
        if update['server_received'] == -1:
            self.insert_in = 10
            self.writer.reset_content()
        elif self.insert_in > 0:
            self.insert_in -= 1
        self.queue.append(update)


    def display_insert(self, update):
        bids, asks = update['bids'], update['asks']
        # start caching for a couple seconds
        self.lock.acquire()
        try:
            if 'Binance' == self.exchange or update['server_received'] == -1:
                print("Resetting content of Orderbook",update["exchange"], "for", update["base"]+update["quote"])
                self.writer.reset_content()
            for bid in bids:
                #print("Inserting in {} bid from {}: {}@{}".format(self.shm, update['exchange'], bid['size'], bid['price']))
                self.writer.set_bid_quantity_at(bid['size'], bid['price'])
            for ask in asks:
                #print("Inserting in {} ask from {}: {}@{}".format(self.shm, update['exchange'], ask['size'], ask['price']))
                self.writer.set_ask_quantity_at(ask['size'], ask['price'])
        except:
            print("Failed to acquire memory!")
            self.lock.release()
            sys.exit(1)
        self.lock.release()
        # if not self.writer.is_sound():
        #     print('Incoherent ORDERBOOK')
        #     pprint(self.writer.snapshot_bids(10))
        #     pprint(self.writer.snapshot_asks(10))
        #     sys.exit()

    def reset_orderbook(self):
        self.writer.reset_content()


def launch_feeder(stream_port, shm_name, exchange, market):
    feeder = OrderbookFeeder(stream_port, shm_name, exchange)
    print("Launching orderbook feeder for", exchange, market)

    def term_signal_handler(sig, frame):
        print("Stopping feeder")
        feeder.stop()
        print("Releasing lock if needed...")
        if feeder.lock.locked():
            feeder.lock.release()

    def feeder_int_signal_handler(sig, frame):
        pass

    signal.signal(signal.SIGTERM, term_signal_handler)
    signal.signal(signal.SIGINT, feeder_int_signal_handler)


    feeder.run()
    return feeder

if __name__ == "__main__":
    print("Starting orderbook feeder process")
    exchange, market = sys.argv[1], sys.argv[2]
    stream = Service.get((Service.exchange == exchange) & (Service.instrument == market))
    shm_name = f"/shm_{exchange}_" + '%08x' % random.randrange(16**8)

    query = Service.update(address=shm_name).where((Service.name == 'OrderbookFeeder') & (Service.instrument == market) & (Service.exchange == exchange))
    query.execute()
    launch_feeder(stream.port, shm_name, exchange, market)