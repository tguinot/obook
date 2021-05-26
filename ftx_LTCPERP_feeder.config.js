module.exports = {
  apps : [{
    name: "Orderbook FTX LTC-PERP",
    script: "python3 -u orderbook_feeder.py FTX \"LTC-PERP\"",
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