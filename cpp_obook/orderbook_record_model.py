import datetime
from orderbook_helper import RtOrderbookReader
import time
import sys
import requests
import os
from decimal import Decimal
from pprint import pprint
from orderbook_helper import RtOrderbookReader
import requests
from models import OrderbookRecord, Currency, Exchange
import umsgpack

orderbook_service_port = os.environ.get("ORDERBOOK_SERVICE_PORT")

# First we ask the orderbook service to start listenning to orderbook updates and fill itself
status = umsgpack.loads(requests.get('http://localhost:{}/start_listenning'.format(orderbook_service_port)).content, raw=False)
print("Orderbook service status:", status)

# Wait for enough exchange data to arrive... 
# time.sleep(3)

# Then we request to know the location of the data in shared memory so we can open it
orderbooks_details = umsgpack.loads(requests.get('http://localhost:{}/shm'.format(orderbook_service_port)).content, raw=False)

exchange_name, instrument, shm_path = orderbooks_details[0]


obh_a = RtOrderbookReader(shm_path)

base = Currency.get(Currency.name == 'BTC')
quote = Currency.get(Currency.name == 'USD')
exchange = Exchange.get(Exchange.name == 'FTX')


def snapshot_orderbook(obh):
	bids_prices, asks_prices = [], []
	bids_sizes, asks_sizes = [], []
	snap = obh.snapshot_bids(100)
	if len(snap) > 0:
		mini, maxi = snap[-1][0], snap[0][0]
		for price, size in snap:
			bids_prices.append(Decimal(price))
			bids_sizes.append(Decimal(size))
			#print("Bid {}@{}".format(size, price))
			if price < mini or price > maxi:
				print("ORDERBOOK BIDS INCOHERENT:", snap)

	snap = obh.snapshot_asks(100)
	if len(snap) > 0:
		maxi, mini = snap[-1][0], snap[0][0]
		for price, size in snap:
			asks_prices.append(Decimal(price))
			asks_sizes.append(Decimal(size))
			#print("Ask {}@{}".format(size, price))
			if price < mini or price > maxi:
				print("ORDERBOOK ASKS INCOHERENT:", snap)

	return bids_sizes, bids_prices, asks_sizes, asks_prices


def save_snapshot(base, quote, exchange, bids_sizes, bids_prices, asks_sizes, asks_prices, ts):
	bid_snap = OrderbookRecord(base=base, quote=quote, exchange=exchange, side='bid', sizes=bids_sizes, prices=bids_prices, timestamp=ts)
	bid_snap.save()
	ask_snap = OrderbookRecord(base=base, quote=quote, exchange=exchange, side='ask', sizes=asks_sizes, prices=asks_prices, timestamp=ts)
	ask_snap.save()


while True:
	ts = datetime.datetime.utcnow()
	print("Taking snapshot...")
	bids_sizes_a, bids_prices_a, asks_sizes_a, asks_prices_a = snapshot_orderbook(obh_a)
	print("Saving snapshot...")
	save_snapshot(base, quote, exchange, bids_sizes_a, bids_prices_a, asks_sizes_a, asks_prices_a, ts)

	time.sleep(0.3)

