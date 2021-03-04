from resilient_orderbook_reader import ResilientOrderbookReader

exchange, instrument = 'FTX', 'BTC/USD'

orderbook_reader = ResilientOrderbookReader(exchange, instrument)

# The nonce is like a version number or update number  like 45980 that you can use to track the evolution of updates
bids_nonce = rdr.bids_nonce()
asks_nonce = rdr.asks_nonce()

while True:
    bids, asks = orderbook_reader.snapshot_whole()

    # Re-check the nonces since it is faster to compare the nonce than the whole content
    new_bids_nonce = rdr.bids_nonce()
    if new_bids_nonce == bids_nonce:
        print("Bids been updated since last loop iteration")

    new_asks_nonce = rdr.asks_nonce()
    if new_asks_nonce == asks_nonce:
        print("Asks been updated since last loop iteration")

    bids_nonce, asks_nonce = new_bids_nonce, new_asks_nonce