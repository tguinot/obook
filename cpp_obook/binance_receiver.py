from binance.client import Client
from binance.websockets import BinanceSocketManager
from decimal import Decimal


class BinanceInterface(object):
	def __init__(self, currencies, key, secret, logger, subscriptions=None, on_orderbook_update=None, on_ignite=None):
		self.on_orderbook_update = on_orderbook_update
		self.on_ignite = on_ignite
		self.client = Client(key, secret)
		self.binance_manager = BinanceSocketManager(self.client)
		self.currencies = currencies
		self.partial = self.binance_manager.start_depth_socket(currencies, self.insert_update)

	def startup(self):
		self.binance_manager.start()

	def insert_update(self, msg):
	    for bid in msg['b']:
	        print("Inserting bid: {}@{}".format(Decimal(bid[1]), Decimal(bid[0])))
	        self.on_orderbook_update(True, Decimal(bid[1]), Decimal(bid[0]))
	    for ask in msg['a']:
	        print("Inserting ask: {}@{}".format(Decimal(ask[1]), Decimal(ask[0])))
	        self.on_orderbook_update(False, Decimal(ask[1]), Decimal(ask[0]))

