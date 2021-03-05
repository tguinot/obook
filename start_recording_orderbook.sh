pm2 start 'python3 -u orderbook_record_model.py FTX "BTC/USD"' --time --name "Orderbook Recorder FTX:BTC/USD"
#pm2 start 'python3 -u orderbook_record_model.py FTX "ETH/USD"' --time --name "Orderbook Recorder FTX:ETH/USD"
pm2 start 'python3 -u orderbook_record_model.py BinanceUS "BTCUSD"' --time --name "Orderbook Recorder BinanceUS:BTCUSD"
#pm2 start 'python3 -u orderbook_record_model.py BinanceUS "ETHUSD"' --time --name "Orderbook Recorder BinanceUS:ETHUSD"
