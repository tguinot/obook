module.exports = {
    apps : [{
      name: "Recorder BinanceUS BTC/USD",
      script: "python3 -u orderbook_record_model.py BinanceUS \"BTC/USD\"",
      env: {
        NODE_ENV: "development",
      },
      env_production: {
        NODE_ENV: "production",
      }
    }]
  }