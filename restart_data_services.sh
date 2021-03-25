pm2 delete "OrderbookBinanceUSBTCUSD"
#pm2 delete "OrderbookBinanceUSETHUSD"
pm2 delete "OrderbookFTXBTC/USD"
pm2 delete "OrderbookFTXBTC-PERP"
#pm2 delete "OrderbookFTXETH/USD"
pm2 delete "LiveDataService"
bash start_live_data_service.sh
bash start_orderbook_service.sh