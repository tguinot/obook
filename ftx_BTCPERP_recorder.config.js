module.exports = {
    apps : [{
      name: "Recorder FTX BTC-PERP",
      script: "python3 -u orderbook_record_model.py FTX \"BTC-PERP\"",
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