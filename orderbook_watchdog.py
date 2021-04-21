from resilient_orderbook_reader import ResilientOrderbookReader
import time
import subprocess
import os
from slack_lib import send_slack_alert
import zmq

orderbook_profiles = [{'exchange': 'BinanceUS', 'instrument': 'BTCUSD'}, {'exchange': 'FTX', 'instrument': 'BTC/USD'}, {'exchange': 'FTX', 'instrument': 'BTC-PERP'}, {'exchange': 'FTX', 'instrument': 'ETH-PERP'}]

orderbook_readers = [ResilientOrderbookReader(prof['exchange'], prof['instrument']) for prof in orderbook_profiles]

# The nonce is like a version number or update number  like 45980 that you can use to track the evolution of updates


nonces = {}
staleness = {}

send_slack_alert("#mm-alerts", "(Re)Starting orderbook watchdog")
while True:
    for reader in orderbook_readers:
        bids_nonce = reader.bids_nonce()
        print("Got bids nonce", bids_nonce, "from", reader.shm, "for", reader.instrument)

        if bids_nonce == nonces.get(reader.exchange+reader.instrument+'bid'):
            staleness[reader.exchange+reader.instrument+'bid'] += 1
        else:
            staleness[reader.exchange+reader.instrument+'bid'] = 0

        asks_nonce = reader.asks_nonce()
        print("Got asks nonce", asks_nonce, "from", reader.shm, "for", reader.instrument)

        if asks_nonce == nonces.get(reader.exchange+reader.instrument+'ask'):
            staleness[reader.exchange+reader.instrument+'ask'] += 1
        else:
            staleness[reader.exchange+reader.instrument+'ask'] = 0

        if staleness[reader.exchange+reader.instrument+'ask'] > 1000 or staleness[reader.exchange+reader.instrument+'bid'] > 1000:
            message = f"[WATCHDOG] Orderbook is stale, refreshing {reader.exchange+reader.instrument}"
            print(message)
            send_slack_alert("#mm-alerts", message)
            try:
                reader.refresh_orderbook()
                staleness[reader.exchange+reader.instrument+'ask'] = 0
                staleness[reader.exchange+reader.instrument+'bid'] = 0
            except Exception as e:
                message = f"[WATCHDOG] Failed to refresh orderbook: {reader.exchange+reader.instrument} ({e}) restarting data services"
                print(message)
                send_slack_alert("#mm-alerts", message)
                subprocess.run(["pm2", "restart", "LiveDataService"])
                subprocess.run(["pm2", "restart", "OrderbookBinanceUSBTCUSD"])
                subprocess.run(["pm2", "restart", "OrderbookFTXBTC/USD"])
                time.sleep(15)
                reader.refresh_orderbook()
                staleness[reader.exchange+reader.instrument+'ask'] = 0
                staleness[reader.exchange+reader.instrument+'bid'] = 0
            if asks_nonce == reader.asks_nonce() or bids_nonce == reader.bids_nonce():
                message = f"[WATCHDOG] Orderbook still stale, restarting data services {reader.exchange+reader.instrument}"
                print(message)
                send_slack_alert("#mm-alerts", message)
                subprocess.run(["pm2", "restart", "LiveDataService"])
                subprocess.run(["pm2", "restart", "OrderbookBinanceUSBTCUSD"])
                subprocess.run(["pm2", "restart", "OrderbookFTXBTC/USD"])
                time.sleep(15)
                reader.refresh_orderbook()
                staleness[reader.exchange+reader.instrument+'ask'] = 0
                staleness[reader.exchange+reader.instrument+'bid'] = 0

        bids, asks = reader.snapshot_whole()
        print("Got whole snapshot from", reader.shm, "for", reader.instrument, "bid length", len(bids), "ask length", len(asks))
        if len(bids) and len(asks) and bids[0] >= asks[0]:
            message = f"[WATCHDOG] Orderbook content crossed {reader.exchange+reader.instrument},  BID: {bids[0]}, ASK: {asks[0]}"
            print(message)

        nonces[reader.exchange+reader.instrument+'bid'] = bids_nonce
        nonces[reader.exchange+reader.instrument+'ask'] = asks_nonce

    # Re-check the nonces since it is faster to compare the nonce than the whole content
    time.sleep(0.01)
