import datetime
from pony.orm import *
from orderbook_helper import RtOrderbookReader
import time
import sys

db = Database()

class OrderbookRecord(db.Entity):
	id = PrimaryKey(int, auto=True)
	name = Required(str)
	exchange = Required(str)
	side = Required(str)
	sizes = Optional(FloatArray)
	prices = Optional(FloatArray)
	timestamp = Required(datetime.datetime, default=datetime.datetime.utcnow)


sql_debug(True)
db.bind(provider='postgres', host='localhost', database='postgres', port=5433)
db.generate_mapping(create_tables=True)


shm_name = sys.argv[1]
obh = RtOrderbookReader(shm_name)

while True:
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

	with db_session:
		OrderbookRecord(name=sys.argv[2], exchange=sys.argv[3], side='bid', sizes=bids_sizes, prices=bids_prices)
		OrderbookRecord(name=sys.argv[2], exchange=sys.argv[3], side='ask', sizes=asks_sizes, prices=asks_prices)

	time.sleep(0.5)

