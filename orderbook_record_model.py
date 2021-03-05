import datetime
from liborderbook.orderbook_helper import RtOrderbookReader
import time
import sys
import requests
import os
from decimal import Decimal
from pprint import pprint
import requests
from models import OrderbookRecord, Currency, Exchange, Service
import umsgpack
import copy


target_exchange, target_instrument = sys.argv[1], sys.argv[2]

orderbook_service_details = Service.get((Service.name == 'OrderbookFeeder') & (Service.exchange == target_exchange) & (Service.instrument == target_instrument))

exchange_name, instrument, shm_path = target_exchange, target_instrument, orderbook_service_details.address
obh_a = RtOrderbookReader(shm_path)

base = Currency.get(Currency.name == target_instrument[:3])
quote = Currency.get(Currency.name == target_instrument[3:].split('/')[-1])
exchange = Exchange.get(Exchange.name == target_exchange)

last_bids, last_asks = None, None
same_count = 0

def snapshot_orderbook(obh):
	global last_bids
	global last_asks
	global same_count

	bids_prices, asks_prices = [], []
	bids_sizes, asks_sizes = [], []
	bids, asks = obh.snapshot_whole(100)
	if bids == last_bids and asks == last_asks:
		same_count += 1
		if same_count > 10:
			print()
			sys.exit(0)
	else:
		same_count = 0

	last_bids, last_asks = copy.deepcopy(bids), copy.deepcopy(asks)


	if len(bids) > 0:
		mini, maxi = bids[-1][0], bids[0][0]
		for price, size in bids:
			bids_prices.append(price)
			bids_sizes.append(size)
			#print("Bid {}@{}".format(size, price))
			if price < mini or price > maxi:
				print("ORDERBOOK BIDS INCOHERENT:", bids)
	if len(asks) > 0:
		maxi, mini = asks[-1][0], asks[0][0]
		for price, size in asks:
			asks_prices.append(price)
			asks_sizes.append(size)
			#print("Ask {}@{}".format(size, price))
			if price < mini or price > maxi:
				print("ORDERBOOK ASKS INCOHERENT:", asks)

	return bids_sizes, bids_prices, asks_sizes, asks_prices


def save_snapshot(base, quote, exchange, bids_sizes, bids_prices, asks_sizes, asks_prices, ts):
	snap = OrderbookRecord(base=base, quote=quote, exchange=exchange, ask_sizes=asks_sizes, ask_prices=asks_prices, bid_sizes=bids_sizes, bid_prices=bids_prices, timestamp=ts)
	snap.save()

if __name__ == "__main__":
	print(f"Starting taking snapshots on {exchange_name}:{instrument} @ {shm_path}")

	while True:
		ts = datetime.datetime.utcnow()

		bids_sizes_a, bids_prices_a, asks_sizes_a, asks_prices_a = snapshot_orderbook(obh_a)
		save_snapshot(base, quote, exchange, bids_sizes_a, bids_prices_a, asks_sizes_a, asks_prices_a, ts)

		time.sleep(0.4)

