from fractions import Fraction
from orderbook_helper import RtOrderbookWriter
import random
import sys
from pprint import pprint
import json
import time
import os
import os
import universal_listenner


class OrderbookFeeder(object):
    def __init__(self, shm, exchange, market):
        self.writer = RtOrderbookWriter(shm)
        self.lstr = universal_listenner.UniversalFeedListenner('127.0.0.1', '4242', exchange, market, 'orderbook', on_receive=self.display_insert)
        print("Starting up Feed Listenner!")
    
    def run(self):
        return self.lstr.run()

    def display_insert(self, update):
        # self.writer.reset_content()
        bids, asks = update['bids'], update['asks']
        # print("Inserting update from", update["exchange"], "for", update["base"]+update["quote"])
        for bid in bids:
            # print("Inserting bid from {}: {}@{}".format(update['exchange'], bid['size'], bid['price']))
            quantity, price = Fraction(bid['size']), Fraction(bid['price'])
            self.writer.set_quantity_at(True, *quantity.as_integer_ratio(), *price.as_integer_ratio())
        for ask in asks:
            quantity, price = Fraction(ask['size']), Fraction(ask['price'])
            # print("Inserting ask from {}: {}@{}".format(update['exchange'], ask['size'], ask['price']))
            self.writer.set_quantity_at(False, *quantity.as_integer_ratio(), *price.as_integer_ratio())
        # if not self.writer.is_sound():
        #     print('Incoherent ORDERBOOK')
        #     pprint(self.writer.snapshot_bids(10))
        #     pprint(self.writer.snapshot_asks(10))
        #     sys.exit()

    def reset_orderbook(self):
        self.writer.reset_content()
