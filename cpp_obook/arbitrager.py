import datetime
from pony.orm import *
from orderbook_helper import RtOrderbookReader
import time
import ccxt
import cexio_keys
import binance_keys
import sys
import requests

shm_paths = requests.get('http://localhost:{}/shm'.format(sys.argv[2])).json()


name = sys.argv[1]
base = name[:3]
asset = name[3:]

shm_name_a, shm_name_b = shm_paths['cexio'], shm_paths['binance']
exchange_a, exchange_b = 'cex', 'binance'


exchanges = {}
parameters = {  'cex': {
                    'apiKey': cexio_keys.key,
                    'uid': cexio_keys.uid,
                    'secret': cexio_keys.secret,
                    'timeout': 30000, 
                    'enableRateLimit': True},
                'binance': {
                    'apiKey': binance_keys.key,
                    'secret': binance_keys.secret,
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
        balance[name] = exchanges[name].fetch_balance()
        print("Instantiated exchange", name)

def order(side, exchange, symbol, amount, price):
    fn = exchanges[exchange].createLimitSellOrder if side == 'sell' else exchanges[exchange].createLimitBuyOrder
    def work():
        order = fn(base+'/'+asset, amount, price)
        try:
            ex.cancel_order(order['id'])
        except ExchangeError as e:
            pass
        print("Status for {} {} order {}@{} at {} is {}".format(side, symbol, exchange, amount, price, exchanges[exchange].fetch_order_status('10092633520')))
    threading.Thread(target=work).start()


def send_orders(top_asks_a, top_bids_a, top_asks_b, top_bids_b, crossed_a, crossed_b):
    available_base_a = balance[exchange_a][base]['free']
    available_asset_a = balance[exchange_a][asset]['free']

    available_base_b = balance[exchange_b][base]['free']
    available_asset_b = balance[exchange_b][asset]['free']

    if crossed_a:
        # Selling A buying B
        buyable_amount = available_base_b / top_asks_b[0][0]
        sellable_amount = available_asset_a
        amount = min(top_asks_b[0][1], top_bids_a[0][1], buyable_amount, sellable_amount)
        print("Buying", amount, "@", top_asks_b[0][0], "on", exchange_b)
        #exchanges[exchange_b].createLimitBuyOrder(name, amount, top_asks_b[0][0])
        order('buy', exchange_b, name, amount, top_asks_b[0][0])
        print("Selling", amount, "@", top_bids_a[0][0], "on", exchange_b)
        #exchanges[exchange_a].createLimitSellOrder(name, amount, top_bids_a[0][0])
        order('sell', exchange_a, name, amount, top_bids_a[0][0])
    elif crossed_b:
        # Selling B buying A
        buyable_amount = available_base_a / top_asks_a[0][0]
        sellable_amount = available_asset_b
        amount = min(top_asks_a[0][1], top_bids_b[0][1], buyable_amount, sellable_amount)
        print("Buying", amount, "@", top_asks_a[0][0], "on", exchange_b)
        # order_a = exchanges[exchange_a].createLimitBuyOrder(name, amount, top_asks_a[0][0])
        order('buy', exchange_a, name, amount, top_asks_a[0][0])
        print("Selling", amount, "@", top_bids_b[0][0], "on", exchange_b)
        # order_b = exchanges[exchange_b].createLimitSellOrder(name, amount, top_bids_b[0][0])
        order('sell', exchange_b, name, amount, top_bids_b[0][0])

    

init_exchanges()

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

