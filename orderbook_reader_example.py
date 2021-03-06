from resilient_orderbook_reader import ResilientOrderbookReader
import time
import zmq
exchange, instrument = 'BinanceUS', 'BTCUSD'
orderbook_reader = ResilientOrderbookReader(exchange, instrument)

# The nonce is like a version number or update number  like 45980 that you can use to track the evolution of updates
bids_nonce = orderbook_reader.bids_nonce()
asks_nonce = orderbook_reader.asks_nonce()
while True:
    bids, asks = orderbook_reader.snapshot_whole()
    print("Got snapshot from", orderbook_reader.shm)

    # Re-check the nonces since it is faster to compare the nonce than the whole content
    #time.sleep(0.01)
