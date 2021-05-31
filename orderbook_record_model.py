import datetime
from liborderbook.orderbook_helper import RtOrderbookReader
import time
import requests
import os
from decimal import Decimal
from pprint import pprint
import requests
import signal
import sys
from models import OrderbookRecord, Currency, Exchange, Service, Instrument, close_db_conn, close_services_db_conn
import umsgpack
from db_inquirer import DatabaseQuerier
import copy


target_exchange, target_instrument = sys.argv[1], sys.argv[2]

db_service_interface = DatabaseQuerier('127.0.0.1', 5678)
orderbook_service_details = db_service_interface.find_service('OrderbookFeeder', instrument=target_instrument, exchange=target_exchange) 

#orderbook_service_details = Service.get((Service.name == 'OrderbookFeeder') & (Service.exchange == target_exchange) & (Service.instrument == target_instrument))

exchange_name, instrument, shm_path = target_exchange, target_instrument, orderbook_service_details.get('address')
obh_a = RtOrderbookReader(shm_path)

exchange = Exchange.get(Exchange.name == target_exchange)
db_instrument = Instrument.get((Instrument.name == target_instrument) & (Instrument.exchange_name == exchange.name))
base = db_instrument.base
quote = db_instrument.quote


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
		if same_count > 20:
			print("Orderbook is stale, exiting")
			sys.exit(0)
	else:
		same_count = 0

	last_bids, last_asks = copy.deepcopy(bids), copy.deepcopy(asks)


	if len(bids) > 0:
		mini, maxi = bids[-1][0], bids[0][0]
		for price, size in bids:
			bids_prices.append(str(price))
			bids_sizes.append(str(size))
			#print("Bid {}@{}".format(size, price))
			if price < mini or price > maxi:
				print("ORDERBOOK BIDS INCOHERENT:", bids)
	if len(asks) > 0:
		maxi, mini = asks[-1][0], asks[0][0]
		for price, size in asks:
			asks_prices.append(str(price))
			asks_sizes.append(str(size))
			#print("Ask {}@{}".format(size, price))
			if price < mini or price > maxi:
				print("ORDERBOOK ASKS INCOHERENT:", asks)

	return bids_sizes, bids_prices, asks_sizes, asks_prices

def sigint_handler(sig, frame):
    print('Closing db_connections')
    close_db_conn()
    close_services_db_conn()
    sys.exit(0)

if __name__ == "__main__":
	print(f"Starting taking snapshots on {exchange_name}:{instrument} @ {shm_path}")
	signal.signal(signal.SIGINT, sigint_handler)
	while True:
		ts = datetime.datetime.utcnow().timestamp()

		bids_sizes_a, bids_prices_a, asks_sizes_a, asks_prices_a = snapshot_orderbook(obh_a)
		db_service_interface.save_snapshot(target_exchange, target_instrument, bids_sizes_a, bids_prices_a, asks_sizes_a, asks_prices_a, ts)

		time.sleep(0.4)

	print("Leaving the for loop")
