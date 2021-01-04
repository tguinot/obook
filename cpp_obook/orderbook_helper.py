from build import orderbook_wrapper
from fractions import Fraction
import random

class RtOrderbookWriter(orderbook_wrapper.OrderbookWriter):
	def __init__(self, path):
		super().__init__()
		print("Instantiated writer ")
		self.init_shm(path)

	def set_bid_quantity_at(self, price, quantity):
		frac_price = Fraction.from_float(price)
		frac_quantity = Fraction.from_float(quantity)
		return super().set_quantity_at(True, frac_quantity.numerator, frac_quantity.denominator, frac_price.numerator, frac_price.denominator)

	def set_ask_quantity_at(self, price, quantity):
		frac_price = Fraction.from_float(price)
		frac_quantity = Fraction.from_float(quantity)
		return super().set_quantity_at(False, frac_quantity.numerator, frac_quantity.denominator, frac_price.numerator, frac_price.denominator)

	def snapshot_bids(self, max_limit=10):
		raw_result = super().snapshot_bids(max_limit)
		result = []
		return [(float(Fraction(*price)), float(Fraction(*qty))) for price, qty in raw_result]

	def snapshot_asks(self, max_limit=10):
		raw_result = super().snapshot_asks(max_limit)
		result = []
		return [(float(Fraction(*price)), float(Fraction(*qty))) for price, qty in raw_result]

	def first_price(self, side):
		price = super().first_price(side)
		return float(Fraction(*price))

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

	def first_price(self, side):
		price = super().first_price(side)
		return float(Fraction(*price))