module.exports = {
    apps : [{
      name: "Recorder FTX BTC/USD",
      script: "python3 -u $HOME/code/obook/orderbook_record_model.py FTX \"BTC/USD\"",
      time: true,
      env: {
        NODE_ENV: "development",
        SHARED_DB_USER: "recorder",
      },
      env_production: {
        NODE_ENV: "production",
        SHARED_DB_USER: "recorder",
      }
    }]
  }