module.exports = {
    apps : [{
      name: "Recorder BinanceUS BTC/USD",
      script: "python3 -u orderbook_record_model.py BinanceUS \"BTCUSD\"",
      env: {
        NODE_ENV: "development",
      },
      env_production: {
        NODE_ENV: "production",
      }
    }]
  }