from orderbook_helper import RtOrderbookWriter
import random
import sys
import threading
from pprint import pprint
import json
import time
import os
from flask import Flask
from markets_config import all_markets
import os
from orderbook_feeder import OrderbookFeeder

app = Flask(__name__)
all_feeders = []


class FeederEntry(object):
    def __init__(self, market):
        self.market = market
        self.exchange = market['exchange']
        self.shm_name = '/shm' + str(random.random())
        self.feeder = OrderbookFeeder(self.shm_name, self.exchange, market)


def generate_shms(markets):
    shm_names = {}
    for market in markets:
        exchange = market['exchange']
        instrument = market['id']
        shm_names[exchange+instrument] = '/shm' + str(random.random())
    return shm_names


@app.route('/shm')
def hello_world():
    return json.dumps([feeder_entry.shm_name for feeder_entry in all_feeders])


if __name__ == "__main__":
    for market in all_markets:
        all_feeders.append(FeederEntry(market))

    def launch_feeder(feeder_entry):
        print("Launching orderbook feeder for", feeder_entry.exchange, feeder_entry.market)
        return feeder_entry.feeder.run()
        
    feeder_threads = []

    for feeder_entry in all_feeders:
        feeder_threads.append(launch_feeder(feeder_entry))

    for feeder_thread in feeder_threads:
        feeder_thread.join()

    print("Started all orderbooks!")

