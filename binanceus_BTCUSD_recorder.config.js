module.exports = {
    apps : [{
      name: "Recorder BinanceUS BTC/USD",
      script: "python3 -u $HOME/code/obook/orderbook_record_model.py BinanceUS \"BTCUSD\"",
      time: true,
      env: {
        NODE_ENV: "development",
        POSTGRES_SERVICES_DB_USER: "recorder",
      },
      env_production: {
        NODE_ENV: "production",
        POSTGRES_SERVICES_DB_USER: "recorder",
      }
    }]
  }