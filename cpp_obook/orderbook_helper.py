from build import orderbook_wrapper
from fractions import Fraction
import random

class RtOrderbookWriter(orderbook_wrapper.OrderbookWriter):
	def __init__(self, path):
		super().__init__()
		self.init_shm(path)

class RtOrderbookReader(orderbook_wrapper.OrderbookReader):
	def __init__(self, path):
		super().__init__()
		self.init_shm(path)

	def snapshot_bids(self, max_limit=10):
		raw_result = super().snapshot_bids(max_limit)
		result = []
		return [(float(Fraction(*price)), float(Fraction(*qty))) for price, qty in raw_result]

	def snapshot_asks(self, max_limit=10):
		raw_result = super().snapshot_asks(max_limit)
		result = []
		return [(float(Fraction(*price)), float(Fraction(*qty))) for price, qty in raw_result]

