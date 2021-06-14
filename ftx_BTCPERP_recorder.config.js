module.exports = {
    apps : [{
      name: "Recorder FTX BTC-PERP",
      script: "python3 -u $HOME/code/obook/orderbook_record_model.py FTX \"BTC-PERP\"",
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