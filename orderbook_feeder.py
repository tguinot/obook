from fractions import Fraction
from liborderbook.orderbook_helper import RtOrderbookWriter
import random
import sys
from pprint import pprint
import json
import time
import os
import os
import universal_listenner


class OrderbookFeeder(object):
    def __init__(self, stream_port, shm, exchange, market):
        self.writer = RtOrderbookWriter(shm)
        self.shm = shm
        self.exchange = exchange
        self.lstr = universal_listenner.UniversalFeedListenner('127.0.0.1', stream_port, exchange, market, 'orderbook', on_receive=self.display_insert)
        print("Starting up Feed Listenner!")
    
    def run(self):
        return self.lstr.run()

    def display_insert(self, update):
        bids, asks = update['bids'], update['asks']
        if self.exchange == 'Binance':
            self.writer.reset_content()
            #print("Inserting update from", update["exchange"], "for", update["base"]+update["quote"])
            #pprint(update)
        for bid in bids:
            # print("Inserting in {} bid from {}: {}@{}".format(self.shm, update['exchange'], bid['size'], bid['price']))
            self.writer.set_bid_quantity_at(bid['size'], bid['price'])
        for ask in asks:
            # print("Inserting in {} ask from {}: {}@{}".format(self.shm, update['exchange'], ask['size'], ask['price']))
            self.writer.set_ask_quantity_at(ask['size'], ask['price'])
        # if not self.writer.is_sound():
        #     print('Incoherent ORDERBOOK')
        #     pprint(self.writer.snapshot_bids(10))
        #     pprint(self.writer.snapshot_asks(10))
        #     sys.exit()

    def reset_orderbook(self):
        self.writer.reset_content()
        