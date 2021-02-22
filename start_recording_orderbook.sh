pm2 start 'python3 -u orderbook_record_model.py FTX "BTC/USD"' --time --name "Orderbook Recorder FTX:BTC/USD"
pm2 start 'python3 -u orderbook_record_model.py FTX "ETH/USD"' --time --name "Orderbook Recorder FTX:ETH/USD"
pm2 start 'python3 -u orderbook_record_model.py Binance "BTCUSDT"' --time --name "Orderbook Recorder Binance:BTCUSDT"
pm2 start 'python3 -u orderbook_record_model.py Binance "ETHUSDT"' --time --name "Orderbook Recorder Binance:ETHUSDT"
