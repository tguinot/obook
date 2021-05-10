module.exports = {
  apps : [{
    name: "Orderbook FTX BTC/USD",
    script: "python3 -u orderbook_feeder.py FTX \"BTC/USD\"",
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