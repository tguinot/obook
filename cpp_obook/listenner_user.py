import universal_listenner

market = {
    "id": "BTC/USD",
    "base": "BTC",
    "quote": "USD",
}

lstr = universal_listenner.UniversalFeedListenner('127.0.0.1', '4242', 'FTX', market, 'orderbook', on_receive=print)
lstr.run()