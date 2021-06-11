module.exports = {
  apps : [{
    name: "Orderbook FTX ETH-PERP",
    script: "python3 -u orderbook_feeder.py FTX \"ETH-PERP\"",
    time: true,
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