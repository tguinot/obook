from build import orderbook_wrapper
from fractions import Fraction
import random


class CommonOrderBookClass:
	def snapshot_bids(self, max_limit=10):
		raw_result = super().snapshot_bids(max_limit)
		return [(float(Fraction(*price)), float(Fraction(*qty))) for price, qty in raw_result]

	def snapshot_asks(self, max_limit=10):
		raw_result = super().snapshot_asks(max_limit)
		return [(float(Fraction(*price)), float(Fraction(*qty))) for price, qty in raw_result]

	def first_price(self, side):
		price = super().first_price(side)
		return float(Fraction(*price))

	def is_sound(self, max_limit=100):
		bids = self.snapshot_bids(max_limit)
		asks = self.snapshot_asks(max_limit)
		if not bids == sorted(bids, key=lambda x: x[0], reverse=True):
			return False
		if not asks == sorted(asks, key=lambda x: x[0]):
			return False
		return True


class RtOrderbookReader(orderbook_wrapper.OrderbookReader, CommonOrderBookClass):
	def __init__(self, path):
		super().__init__()
		self.init_shm(path)

	
class RtOrderbookWriter(orderbook_wrapper.OrderbookWriter, CommonOrderBookClass):
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