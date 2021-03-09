from resilient_orderbook_reader import ResilientOrderbookReader
import time
import subprocess
import zmq

orderbook_profiles = [{'exchange': 'BinanceUS', 'instrument': 'BTCUSD'}]#, {'exchange': 'FTX', 'instrument': 'BTC/USD'}]

orderbook_readers = [ResilientOrderbookReader(prof['exchange'], prof['instrument']) for prof in orderbook_profiles]

# The nonce is like a version number or update number  like 45980 that you can use to track the evolution of updates

nonces = {}
staleness = {}
while True:
    for reader in orderbook_readers:
        bids_nonce = reader.bids_nonce()
        print("Got bids nonce", bids_nonce, "from", reader.shm, "for", reader.instrument)

        if bids_nonce == nonces.get(reader.exchange+reader.instrument+'bid'):
            staleness[reader.exchange+reader.instrument+'bid'] += 1
        else:
            staleness[reader.exchange+reader.instrument+'bid'] = 0

        if staleness[reader.exchange+reader.instrument+'bid'] > 3000:
            print("Orderbook", reader.exchange+reader.instrument+'bid', 'is stale')
            reader.refresh_orderbook()

        asks_nonce = reader.asks_nonce()
        print("Got asks nonce", asks_nonce, "from", reader.shm, "for", reader.instrument)

        if asks_nonce == nonces.get(reader.exchange+reader.instrument+'ask'):
            staleness[reader.exchange+reader.instrument+'ask'] += 1
        else:
            staleness[reader.exchange+reader.instrument+'ask'] = 0

        if staleness[reader.exchange+reader.instrument+'ask'] > 1000:
            print("Orderbook", reader.exchange+reader.instrument+'ask', 'is stale')
            try:
                reader.refresh_orderbook()
                staleness[reader.exchange+reader.instrument+'ask'] = 0
                staleness[reader.exchange+reader.instrument+'bid'] = 0
            except Exception as e:
                print("Failed to refresh orderbook:", e, "restarting data services")
                subprocess.run(["pm2", "restart", "LiveDataService"])
                subprocess.run(["pm2", "restart", "OrderbookBinanceUSBTCUSD"])
                time.sleep(15)
                reader.refresh_orderbook()
                staleness[reader.exchange+reader.instrument+'ask'] = 0
                staleness[reader.exchange+reader.instrument+'bid'] = 0
            if asks_nonce == reader.asks_nonce() or bids_nonce == reader.bids_nonce():
                print("Orderbook still stale, restarting data services")
                subprocess.run(["pm2", "restart", "LiveDataService"])
                subprocess.run(["pm2", "restart", "OrderbookBinanceUSBTCUSD"])
                time.sleep(15)
                reader.refresh_orderbook()
                staleness[reader.exchange+reader.instrument+'ask'] = 0
                staleness[reader.exchange+reader.instrument+'bid'] = 0


        bids, asks = reader.snapshot_whole()
        print("Got whole snapshot from", reader.shm, "for", reader.instrument, "bid length", len(bids), "ask length", len(asks))

        nonces[reader.exchange+reader.instrument+'bid'] = bids_nonce
        nonces[reader.exchange+reader.instrument+'ask'] = asks_nonce

    # Re-check the nonces since it is faster to compare the nonce than the whole content
    time.sleep(0.01)
