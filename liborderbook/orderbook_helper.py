from . import orderbook_wrapper
from fractions import Fraction
from decimal import Decimal
import random


class CommonOrderBookClass:
	def is_sound(self, max_limit=100):
		bids = self.snapshot_bids(max_limit)
		asks = self.snapshot_asks(max_limit)
		if len(bids) and len(asks) and (bids[0] >= asks[0]):
			print("BIDS HIGHER THAN ASKS", bids[0], "vs", asks[0])
			return False
		if not bids == sorted(bids, key=lambda x: x[0], reverse=True):
			return False
		if not asks == sorted(asks, key=lambda x: x[0]):
			return False
		return True

def dec(n, d):
	return Decimal(n) / Decimal(d)




class RtOrderbookReader(orderbook_wrapper.OrderbookReader, CommonOrderBookClass):
	def __init__(self, path):
		super().__init__()
		self.init_shm(path)

	def snapshot_bids(self, max_limit=10):
		raw_result = super().snapshot_bids(max_limit)
		return [(dec(*price), dec(*qty)) for price, qty in raw_result]

	def snapshot_asks(self, max_limit=10):
		raw_result = super().snapshot_asks(max_limit)
		return [(dec(*price), dec(*qty)) for price, qty in raw_result]

	def snapshot_whole(self, max_limit=10):
		frac_bids, frac_asks = super().snapshot_whole(max_limit)
		def frac_sidebook_to_decimals(sidebook):
			result = []
			for entry in sidebook:
				frac_price, frac_qty = entry
				price, qty = dec(*frac_price), dec(*frac_qty)
				result.append([price, qty])
			return result

		bids = frac_sidebook_to_decimals(frac_bids)
		asks = frac_sidebook_to_decimals(frac_asks)
		return bids, asks

	def first_price(self, side):
		price = super().first_price(side)
		return dec(*price)

	
class RtOrderbookWriter(orderbook_wrapper.OrderbookWriter, CommonOrderBookClass):
	def __init__(self, path):
		super().__init__()
		self.init_shm(path)

	def snapshot_bids(self, max_limit=10):
		raw_result = super().snapshot_bids(max_limit)
		return [(dec(*price), dec(*qty)) for price, qty in raw_result]

	def snapshot_asks(self, max_limit=10):
		raw_result = super().snapshot_asks(max_limit)
		return [(dec(*price), dec(*qty)) for price, qty in raw_result]

	def snapshot_whole(self, max_limit=10):
		frac_bids, frac_asks = super().snapshot_whole(max_limit)
		def frac_sidebook_to_decimals(sidebook):
			result = []
			for entry in sidebook:
				frac_price, frac_qty = entry
				price, qty = dec(*frac_price), dec(*frac_qty)
				result.append([price, qty])
			return result

		bids = frac_sidebook_to_decimals(frac_bids)
		asks = frac_sidebook_to_decimals(frac_asks)
		return bids, asks

	def set_bid_quantity_at(self, quantity, price):
		frac_price = Fraction(price)
		frac_quantity = Fraction(quantity)
		return super().set_quantity_at(True, frac_quantity.numerator, frac_quantity.denominator, frac_price.numerator, frac_price.denominator)

	def set_ask_quantity_at(self, quantity, price):
		frac_price = Fraction(price)
		frac_quantity = Fraction(quantity)
		return super().set_quantity_at(False, frac_quantity.numerator, frac_quantity.denominator, frac_price.numerator, frac_price.denominator)

	def set_ask_quantities_at(self, quantities, prices):
		frac_quantities, frac_prices = [], []
		for quantity, price in zip(quantities, prices):
			frac_price = Fraction(price)
			frac_quantity = Fraction(quantity)
			frac_quantities.append((frac_quantity.numerator, frac_quantity.denominator))
			frac_prices.append((frac_price.numerator, frac_price.denominator))
		return super().set_quantities_at(False, frac_quantities,  frac_prices)

	def set_bid_quantities_at(self, quantities, prices):
		frac_quantities, frac_prices = [], []
		for quantity, price in zip(quantities, prices):
			frac_price = Fraction(price)
			frac_quantity = Fraction(quantity)
			frac_quantities.append((frac_quantity.numerator, frac_quantity.denominator))
			frac_prices.append((frac_price.numerator, frac_price.denominator))
		return super().set_quantities_at(True, frac_quantities,  frac_prices)

	def first_price(self, side):
		price = super().first_price(side)
		return dec(*price)