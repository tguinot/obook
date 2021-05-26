module.exports = {
  apps : [{
    name: "Orderbook FTX BNB-PERP",
    script: "python3 -u orderbook_feeder.py FTX \"BNB-PERP\"",
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