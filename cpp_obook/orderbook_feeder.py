from cexio_receiver import CexioInterface
from binance_receiver import BinanceInterface
from trade_logger import get_logger
from cexio_keys import key, secret
#from build import orderbook_wrapper
from fractions import Fraction
from orderbook_helper import RtOrderbookWriter
import random
import sys

interfaces = {'cexio': CexioInterface,
			  'binance': BinanceInterface}

shm_name = '/shm' + str(random.random())
writer = RtOrderbookWriter(shm_name)

def display_insert(side, quantity, price):
    print("Inserting {}: {}@{} of types {} {} ".format(side, quantity, price, type(quantity), type(price)))
    writer.set_quantity_at(side, *quantity.as_integer_ratio(), *price.as_integer_ratio())

def reset_orderbook():
	writer.reset_content()

print('SHM path is', shm_name)
cexio_logger = get_logger('Man Trade', 'mantrader.log')
iface_name = sys.argv[1]
instrument = sys.argv[2]
iface = interfaces[iface_name](instrument, key, secret, cexio_logger, subscriptions=["orderbook"], on_orderbook_update=display_insert, on_ignite=reset_orderbook)
iface.startup()
print("Started !")

