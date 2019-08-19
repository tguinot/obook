import datetime
from pony.orm import *
from orderbook_helper import RtOrderbookReader
import time
import sys
import requests

db = Database()

class OrderbookRecord(db.Entity):
	id = PrimaryKey(int, auto=True)
	name = Required(str)
	exchange = Required(str)
	side = Required(str)
	sizes = Optional(FloatArray)
	prices = Optional(FloatArray)
	timestamp = Required(datetime.datetime)

shm_paths = requests.get('http://localhost:{}/shm'.format(sys.argv[5])).json()


name = sys.argv[1]
database = sys.argv[2]
port = sys.argv[3]
password = sys.argv[4]

sql_debug(True)
db.bind(provider='postgres', host='localhost', database=database, port=int(port), password=password)
db.generate_mapping(create_tables=True)


shm_name_a, shm_name_b = shm_paths['cexio'], shm_paths['binance']
exchange_a, exchange_b = 'cexio', 'binance'


obh_a, obh_b = RtOrderbookReader(shm_name_a), RtOrderbookReader(shm_name_b)


def snapshot_orderbook(obh):
	bids_prices, asks_prices = [], []
	bids_sizes, asks_sizes = [], []
	snap = obh.snapshot_bids()
	if len(snap) > 0:
		mini, maxi = snap[-1][0], snap[0][0]
		for price, size in snap:
			bids_prices.append(price)
			bids_sizes.append(size)
			print("Bid {}@{}".format(size, price))
			if price < mini or price > maxi:
				print("ORDERBOOK BIDS INCOHERENT:", snap)

	snap = obh.snapshot_asks()
	if len(snap) > 0:
		maxi, mini = snap[-1][0], snap[0][0]
		for price, size in snap:
			asks_prices.append(price)
			asks_sizes.append(size)
			print("Ask {}@{}".format(size, price))
			if price < mini or price > maxi:
				print("ORDERBOOK ASKS INCOHERENT:", snap)

	return bids_sizes, bids_prices, asks_sizes, asks_prices


def save_snapshot(name, exchange, bids_sizes, bids_prices, asks_sizes, asks_prices, ts):
	OrderbookRecord(name=name, exchange=exchange, side='bid', sizes=bids_sizes, prices=bids_prices, timestamp=ts)
	OrderbookRecord(name=name, exchange=exchange, side='ask', sizes=asks_sizes, prices=asks_prices, timestamp=ts)


while True:
	ts = datetime.datetime.utcnow()
	bids_sizes_a, bids_prices_a, asks_sizes_a, asks_prices_a = snapshot_orderbook(obh_a)
	bids_sizes_b, bids_prices_b, asks_sizes_b, asks_prices_b = snapshot_orderbook(obh_b)
	with db_session:
		save_snapshot(name, exchange_a, bids_sizes_a, bids_prices_a, asks_sizes_a, asks_prices_a, ts)
		save_snapshot(name, exchange_b, bids_sizes_b, bids_prices_b, asks_sizes_b, asks_prices_b, ts)

	time.sleep(0.5)

