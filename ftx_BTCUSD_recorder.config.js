module.exports = {
    apps : [{
      name: "Recorder FTX BTC/USD",
      script: "python3 -u orderbook_record_model.py FTX \"BTC/USD\"",
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