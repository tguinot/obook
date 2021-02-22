#from orderbook_helper import RtOrderbookWriter
from liborderbook.orderbook_helper import RtOrderbookWriter
import random
import sys
import threading
from pprint import pprint
import json
import time
import umsgpack
import os
from flask import Flask
from liborderbook.markets_config import all_markets
import os
from orderbook_feeder import OrderbookFeeder
from collections import namedtuple

app = Flask(__name__)
all_feeders = []
started = False

SHMDetail = namedtuple('SHMDetail', 'exchange instrument shm_path')

class FeederEntry(object):
    def __init__(self, market):
        self.market = market
        self.exchange = market['exchange']
        self.shm_name = '/shm_%04x' % random.randrange(16**4)
        self.feeder = OrderbookFeeder(self.shm_name, self.exchange, market)

def generate_shms(markets):
    shm_names = {}
    for market in markets:
        exchange = market['exchange']
        instrument = market['id']
        shm_names[exchange+instrument] = '/shm' + str(random.random())
    return shm_names


@app.route('/shm')
def dump_shm_paths():
    all_details = [SHMDetail(feeder_entry.exchange, feeder_entry.market['id'], feeder_entry.shm_name) for feeder_entry in all_feeders ]
    return umsgpack.dumps(all_details)

feeder_threads = []

@app.route('/start_listenning')
def start_listenning():
    global started
    if started:
        return umsgpack.dumps("All orderbooks started")

    for market in all_markets:
        all_feeders.append(FeederEntry(market))

    def launch_feeder(feeder_entry):
        print("Launching orderbook feeder for", feeder_entry.exchange, feeder_entry.market)
        return feeder_entry.feeder.run()

    for feeder_entry in all_feeders:
        feeder_threads.append(launch_feeder(feeder_entry))

    started = True
    return umsgpack.dumps("Started all orderbooks!")

