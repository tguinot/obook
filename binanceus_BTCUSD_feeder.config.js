module.exports = {
    apps : [{
      name: "Orderbook BinanceUSD BTCUSD",
      script: "python3 -u orderbook_feeder.py BinanceUS BTCUSD",
      env: {
        NODE_ENV: "development",
      },
      env_production: {
        NODE_ENV: "production",
      }
    }]
  }