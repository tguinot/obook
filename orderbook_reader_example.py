from resilient_orderbook_reader import ResilientOrderbookReader
import time

exchange, instrument = 'FTX', 'BTC/USD'
orderbook_reader = ResilientOrderbookReader(exchange, instrument)

# The nonce is like a version number or update number  like 45980 that you can use to track the evolution of updates
bids_nonce = orderbook_reader.bids_nonce()
asks_nonce = orderbook_reader.asks_nonce()

while True:
    bids, asks = orderbook_reader.snapshot_whole()

    # Re-check the nonces since it is faster to compare the nonce than the whole content
    new_bids_nonce = orderbook_reader.bids_nonce()
    if new_bids_nonce == bids_nonce:
        print("Bids have not been updated since last loop iteration")

    new_asks_nonce = orderbook_reader.asks_nonce()
    if new_asks_nonce == asks_nonce:
        print("Asks have not been updated since last loop iteration")

    if new_asks_nonce == asks_nonce and new_bids_nonce == bids_nonce:
        print("No update in 5 seconds, I'm gonna assume the orderbook is stale and needs manual refreshing")
        orderbook_reader.refresh_orderbook()
    else:
        print("Everything normal")

    bids_nonce, asks_nonce = new_bids_nonce, new_asks_nonce
    time.sleep(5)