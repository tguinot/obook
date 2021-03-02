pm2 start 'python3 -u orderbook_feeder.py BinanceUS ETHUSD' --time --name "Orderbook BinanceUS:ETH/USD"
pm2 start 'python3 -u orderbook_feeder.py BinanceUS BTCUSD' --time --name "Orderbook BinanceUS:BTC/USD"
pm2 start 'python3 -u orderbook_feeder.py FTX "BTC/USD"' --time --name "Orderbook FTX:BTC/USD"
pm2 start 'python3 -u orderbook_feeder.py FTX "ETH/USD"' --time --name "Orderbook FTX:ETH/USD"