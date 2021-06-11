module.exports = {
    apps : [{
      name: "Orderbook BinanceUS BTCUSD",
      script: "python3 -u orderbook_feeder.py BinanceUS BTCUSD",
      time: true,
      env: {
        NODE_ENV: "development",
        POSTGRES_SERVICES_DB_USER: "orderbook_feeder",
      },
      env_production: {
        NODE_ENV: "production",
        POSTGRES_SERVICES_DB_USER: "orderbook_feeder",
      }
    }]
  }