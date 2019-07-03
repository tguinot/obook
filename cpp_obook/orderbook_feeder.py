from cexio_receiver import CexioInterface
from trade_logger import get_logger
from build import orderbook_wrapper
from fractions import Fraction
import random

class RtOrderbookWriter(orderbook_wrapper.OrderbookWriter):
	def __init__(self, path):
		super().__init__()
		self.init_shm(path)

shm_name = '/shm' + str(random.random())
writer = RtOrderbookWriter(shm_name)
print("Inited SHM on", shm_name)
cexio_logger = get_logger('Man Trade', 'mantrader.log')

def display_insert(side, quantity, price):
    print("Inserting {}: {}@{} of types {} {} ".format(side, quantity, price, type(quantity), type(price)))
    writer.set_quantity_at(side, *quantity.as_integer_ratio(), *price.as_integer_ratio())

iface = CexioInterface("ETHUSD", "wJ6I0SY7BtbtMtmCFdWYLRGBilw", "6sKWfLRFYTItRzW2QYtwdWIqNM", cexio_logger, subscriptions=["orderbook"], on_orderbook_update=display_insert)
iface.startup()