from trade_logger import get_logger
from fractions import Fraction
from orderbook_helper import RtOrderbookWriter
import random
import sys
import threading
import json
import time
import os
from flask import Flask
import os
import universal_listenner

app = Flask(__name__)


def generate_shms(exchanges):
    shm_names = {}
    for exchange in exchanges:
        shm_names[exchange] = '/shm' + str(random.random())
    return shm_names

@app.route('/shm')
def hello_world():
    return json.dumps(shm_names)


class OrderbookFeeder(object):
    def __init__(self, shm, exchange, market):
        print('SHM path is', str(shm))
        self.writer = RtOrderbookWriter(shm)
        self.lstr = universal_listenner.UniversalFeedListenner('127.0.0.1', '4242', 'Binance', market, 'orderbook', on_receive=self.display_insert)
        print("Starting up Feed Listenner!")
    
    def run(self):
        self.lstr.run()

    def display_insert(self, side, quantity, price):
        print("Inserting from {} {}: {}@{}".format(exchange, side, quantity, price))
        self.writer.set_quantity_at(side, *quantity.as_integer_ratio(), *price.as_integer_ratio())

    def reset_orderbook(self):
        self.writer.reset_content()

all_feeders = []

def launch_feeder(shm_name, exchange, market):
    feeder = OrderbookFeeder(shm_name, exchange, market)
    print("Saving orderbook feeder for", exchange, market)
    all_feeders.append(feeder)
    feeder.run()
    while True:
        time.sleep(2)


if __name__ == "__main__":
    market = {
        "id": "BTCUSDT",
        "base": "BTC",
        "quote": "USDT",
    }

    exchanges = ['binance']

    shm_names = generate_shms(exchanges)

    for exchange, shm_name in shm_names.items():
        p = threading.Thread(target=launch_feeder, args=(shm_name, exchange, market))
        p.start()


    print("Started all orderbooks!")

