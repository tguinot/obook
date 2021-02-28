#from orderbook_helper import RtOrderbookWriter
from liborderbook.orderbook_helper import RtOrderbookWriter
import random
import sys
from multiprocessing import Process
from pprint import pprint
import json
import time
import umsgpack
import signal
import os
from flask import Flask
from models import Service
from orderbook_feeder import OrderbookFeeder
from collections import namedtuple

app = Flask(__name__)
all_feeders = []
started = False


with open('markets_config.json', 'r') as f:
    all_markets = json.load(f)['all_markets']

SHMDetail = namedtuple('SHMDetail', 'exchange instrument shm_path')


class FeederEntry(object):
    def __init__(self, market, stream_port):
        self.market = market
        self.exchange = market['exchange']
        self.shm_name = '/shm_%04x' % random.randrange(16**4)
        self.stream_port = stream_port

def generate_shms(markets):
    shm_names = {}
    for market in markets:
        exchange = market['exchange']
        instrument = market['id']
        shm_names[exchange+instrument] = '/shm' + str(random.random())
        print(f"Generated shm for {exchange+instrument} at {shm_names[exchange+instrument]}")
    return shm_names


@app.route('/shm')
def dump_shm_paths():
    print("Received SHM request...")
    all_details = [SHMDetail(feeder_entry.exchange, feeder_entry.market['id'], feeder_entry.shm_name) for feeder_entry in all_feeders ]
    return umsgpack.dumps(all_details)

feeder_procs = []

for market in all_markets:
    stream = Service.get((Service.exchange == market['exchange']) & (Service.instrument == market['id']))
    print("Fetched stream port", stream.port, "for", market)
    all_feeders.append(FeederEntry(market, stream.port))

def launch_feeder(feeder_entry):
    feeder = OrderbookFeeder(feeder_entry.stream_port, feeder_entry.shm_name, feeder_entry.exchange, market)
    print("Launching orderbook feeder for", feeder_entry.exchange, feeder_entry.market)

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

for feeder_entry in all_feeders:
    p = Process(target=launch_feeder, args=(feeder_entry,))
    p.start()
    feeder_procs.append(p)


def int_signal_handler(sig, frame):
    for p in feeder_procs:
        print("Attempting terminating feeder process...")
        p.terminate()
        p.join()
    sys.exit(0)


signal.signal(signal.SIGINT, int_signal_handler)


started = True

@app.route('/start_listenning')
def start_listenning():
    global started
    if started:
        return umsgpack.dumps("All orderbooks started")

    return umsgpack.dumps("Orderbooks not started")

