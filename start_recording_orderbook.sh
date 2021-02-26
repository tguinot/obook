pm2 start 'python3 -u orderbook_record_model.py FTX "BTC/USD"' --time --name "Orderbook Recorder FTX:BTC/USD"
pm2 start 'python3 -u orderbook_record_model.py FTX "ETH/USD"' --time --name "Orderbook Recorder FTX:ETH/USD"
pm2 start 'python3 -u orderbook_record_model.py BinanceUS "BTCUSDT"' --time --name "Orderbook Recorder BinanceUS:BTCUSDT"
pm2 start 'python3 -u orderbook_record_model.py BinanceUS "ETHUSDT"' --time --name "Orderbook Recorder BinanceUS:ETHUSDT"
