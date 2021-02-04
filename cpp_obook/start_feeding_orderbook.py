from orderbook_helper import RtOrderbookWriter
import random
import sys
import threading
from pprint import pprint
import json
import time
import os
from flask import Flask
import os
from orderbook_feeder import OrderbookFeeder

app = Flask(__name__)


def generate_shms(exchanges):
    shm_names = {}
    for exchange in exchanges:
        shm_names[exchange] = '/shm' + str(random.random())
    return shm_names

@app.route('/shm')
def hello_world():
    return json.dumps(shm_names)


if __name__ == "__main__":
    market = {
        "id": "BTC/USD",
        "base": "BTC",
        "quote": "USD",
    }

    exchanges = ['FTX']

    all_feeders = []

    def launch_feeder(shm_name, exchange, market):
        feeder = OrderbookFeeder(shm_name, exchange, market)
        print("Saving orderbook feeder for", exchange, market)
        all_feeders.append(feeder)
        feeder.run()
        while True:
            time.sleep(2)

    shm_names = generate_shms(exchanges)

    for exchange, shm_name in shm_names.items():
        p = threading.Thread(target=launch_feeder, args=(shm_name, exchange, market))
        p.start()

    print("Started all orderbooks!")

