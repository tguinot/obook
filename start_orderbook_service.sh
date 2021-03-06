pm2 start 'python3 -u orderbook_feeder.py BinanceUS ETHUSD' --time --name "OrderbookBinanceUSETHUSD"
pm2 start 'python3 -u orderbook_feeder.py BinanceUS BTCUSD' --time --name "OrderbookBinanceUSBTCUSD"
pm2 start 'python3 -u orderbook_feeder.py FTX "BTC/USD"' --time --name "OrderbookFTXBTC/USD"
pm2 start 'python3 -u orderbook_feeder.py FTX "ETH/USD"' --time --name "OrderbookFTXETH/USD"