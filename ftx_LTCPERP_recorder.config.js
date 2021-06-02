module.exports = {
    apps : [{
      name: "Recorder FTX LTC-PERP",
      script: "python3 -u orderbook_record_model.py FTX \"LTC-PERP\"",
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