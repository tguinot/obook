import datetime
from pony.orm import *
from orderbook_helper import RtOrderbookReader
import time
import ccxt
import threading
from pprint import pprint
import sys
import time
import requests
from math import floor, ceil


shm_port = os.environ.get("SHM_PORT")

# shm_paths = requests.get('http://localhost:{}/shm'.format(sys.argv[2])).json()
shm_paths = requests.get('http://localhost:{}/shm'.format(shm_port)).json()

# name = sys.argv[1]
name = os.environ.get("INSTRUMENT")

asset = name[:3]
base = name[3:]

binance_key = os.environ.get("BINANCE_KEY")
binance_secret = os.environ.get("BINANCE_SECRET")

cexio_key = os.environ.get("CEXIO_KEY")
cexio_secret = os.environ.get("CEXIO_SECRET")
cexio_uid = os.environ.get("CEXIO_UID")

shm_name_a, shm_name_b = shm_paths['cexio'], shm_paths['binance']
exchange_a, exchange_b = 'cex', 'binance'

min_amounts = {
    'ETHBTC': 0.05,
    'LTCBTC': 0.05,
}


exchanges = {}
parameters = {  'cex': {
                    'apiKey': cexio_key,
                    'uid': cexio_uid,
                    'secret': cexio_secret,
                    'timeout': 30000, 
                    'enableRateLimit': True},
                'binance': {
                    'apiKey': binance_key,
                    'secret': binance_secret,
                    'timeout': 30000, 
                    'enableRateLimit': True}
}

obh_a, obh_b = RtOrderbookReader(shm_name_a), RtOrderbookReader(shm_name_b)

balance = {}

def crossing_ongoing(top_bids_a, top_asks_a, top_bids_b, top_asks_b, max_offset_pct=-0.2):
    if len(top_asks_a) < 1  or len(top_bids_a) < 1:
        return False, False
    if len(top_asks_b) < 1  or len(top_bids_b) < 1:
        return False, False
    cross_a = 100*((top_asks_b[0][0]/top_bids_a[0][0])-1)
    cross_b = 100*((top_asks_a[0][0]/top_bids_b[0][0])-1)

    return cross_a <= max_offset_pct, cross_b <= max_offset_pct


def init_exchanges():
    for name in [exchange_a, exchange_b]:
        exchange_class = getattr(ccxt, name)
        if not exchange_class:
            continue 
        exchanges[name] = exchange_class(parameters[name])
        if name == 'cex':
            exchanges[name].options['createMarketBuyOrderRequiresPrice'] = False
        balance[name] = exchanges[name].fetch_balance()
        print("Instantiated exchange", name)


def roundDown(n, d=4):
    d = int('1' + ('0' * d))
    return floor(n * d) / d

def order(side, exchange, symbol, amount, price):
    fn = exchanges[exchange].createLimitSellOrder if side == 'sell' else exchanges[exchange].createLimitBuyOrder

    def work():
        try:
            order = fn(asset+'/'+base, amount, price)
            print("Order",  order['id'], "passed on", exchange)
            pprint(order)
        except Exception as e:
            print("Could not place order:", asset+'/'+base, amount, price, e)
            return
        try:
            ex.cancel_order(order['id'])
        except Exception as e:
            print("Could not cancel order:", order['id'])
        print("Status for {} {} order {}@{} on {} is {}".format(side, symbol, exchange, amount, price, exchanges[exchange].fetch_order_status(order['id'], asset+'/'+base)))
    threading.Thread(target=work).start()
    

def refresh():
    time.sleep(4)
    for name in [exchange_a, exchange_b]:
        balance[name] = exchanges[name].fetch_balance()

def continuously_refresh():
    while True:
        for name in [exchange_a, exchange_b]:
            try:
                balance[name] = exchanges[name].fetch_balance()
            except:
                pass
    time.sleep(7)


def fetch_exchanges_balance_summary():
    a = {k:v for k,v in exchanges[exchange_a].fetch_balance()['free'].items() if v > 0}
    b = {k:v for k,v in exchanges[exchange_b].fetch_balance()['free'].items() if v > 0}
    return a, b


def print_balances_summary():
    balances = fetch_exchanges_balance_summary()
    print("Balance of", exchange_a, ":")
    print(balances[0])
    print("Balance of", exchange_b, ":")
    print(balances[1])


def prepare_and_send(top_asks, top_bids, available_base, available_asset):
    buyable_amount = available_base / top_asks[0][0]
    sellable_amount = available_asset
    amount = roundDown(min(top_asks[0][1], top_bids[0][1], buyable_amount, sellable_amount))
    if amount < min_amounts[name]:
        print("Too small opportunity", name, amount)
        return
    print("A-Way Available buyable/sellable amounts are", available_base, base, sellable_amount, asset, "with price", top_asks[0][0])
    print("Buying", amount, "@", top_asks[0][0], "on", exchange)
    order('buy', exchange, name, amount, top_asks[0][0])
    print("Selling", amount, "@", top_bids[0][0], "on", exchange)
    order('sell', exchange, name, amount, top_bids[0][0])


def send_orders(top_asks_a, top_bids_a, top_asks_b, top_bids_b, crossed_a, crossed_b):
    available_base_a = balance[exchange_a][base]['free']
    available_asset_a = balance[exchange_a][asset]['free']

    available_base_b = balance[exchange_b][base]['free']
    available_asset_b = balance[exchange_b][asset]['free']

    if crossed_a:
        prepare_and_send(top_asks_b, top_bids_a, available_base_b, available_asset_a)

        # buyable_amount = available_base_b / top_asks_b[0][0]
        # sellable_amount = available_asset_a
        # amount = roundDown(min(top_asks_b[0][1], top_bids_a[0][1], buyable_amount, sellable_amount))
        # if amount < min_amounts[name]:
        #     print("Too small opportunity", name, amount)
        #     return
        # print("A-Way Available buyable/sellable amounts are", available_base_b, base, sellable_amount, asset, "with price", top_asks_b[0][0])
        # print("Buying", amount, "@", top_asks_b[0][0], "on", exchange_b)
        # order('buy', exchange_b, name, amount, top_asks_b[0][0])
        # print("Selling", amount, "@", top_bids_a[0][0], "on", exchange_a)
        # order('sell', exchange_a, name, amount, top_bids_a[0][0])

    elif crossed_b:
        prepare_and_send(top_asks_a, top_bids_b, available_base_a, available_asset_b)

        # buyable_amount = available_base_a / top_asks_a[0][0]
        # sellable_amount = available_asset_b
        # amount = roundDown(min(top_asks_a[0][1], top_bids_b[0][1], buyable_amount, sellable_amount))
        # if amount < min_amounts[name]:
        #     print("Too small opportunity", name, amount)
        #     return
        # print("B-Way Available buyable/sellable amounts are", available_base_a, base, sellable_amount, asset, "with price", top_asks_a[0][0])
        # print("Buying", amount, asset, "@", top_asks_a[0][0], base, "on", exchange_a)
        # order('buy', exchange_a, name, amount, top_asks_a[0][0])
        # print("Selling", amount, asset, "@", top_bids_b[0][0], base, "on", exchange_b)
        # order('sell', exchange_b, name, amount, top_bids_b[0][0])
    refresh()

    

init_exchanges()
print_balances_summary()
threading.Thread(target=continuously_refresh).start()

while True:
    ts = datetime.datetime.utcnow()
    top_asks_a, top_bids_a = obh_a.snapshot_asks(max_limit=1), obh_a.snapshot_bids(max_limit=1)
    top_asks_b, top_bids_b = obh_b.snapshot_asks(max_limit=1), obh_b.snapshot_bids(max_limit=1)

    crossed_a, crossed_b =  crossing_ongoing(top_bids_a, top_asks_a, top_bids_b, top_asks_b, max_offset_pct=-0.5)
    if crossed_a or crossed_b:
        print("Crossing status @ {}: {} B: {} VS {} A:{}  ({}%) -------  {} B: {} VS {} A:{} ({}%)".format( 
            ts, exchange_a, top_bids_a, exchange_b, top_asks_b, 100*((top_asks_b[0][0]/top_bids_a[0][0])-1),
            exchange_b, top_bids_b, exchange_a, top_asks_a, 100*((top_asks_a[0][0]/top_bids_b[0][0])-1)))
        send_orders(top_asks_a, top_bids_a, top_asks_b, top_bids_b, crossed_a, crossed_b)

    time.sleep(0.01)

