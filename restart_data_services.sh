pm2 delete "OrderbookBinanceUSBTCUSD"
#pm2 delete "OrderbookBinanceUSETHUSD"
pm2 delete "OrderbookFTXBTC/USD"
pm2 delete "OrderbookFTXBTC-PERP"
#pm2 delete "OrderbookFTXETH/USD"
pm2 delete "LiveDataService"
pm2 delete "OrderbookWatchDog"
bash start_all_services.sh