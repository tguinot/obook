module.exports = {
  apps : [{
    name: "Orderbook FTX XRP-PERP",
    script: "python3 -u orderbook_feeder.py FTX \"XRP-PERP\"",
    env: {
      NODE_ENV: "development",
    },
    env_production: {
      NODE_ENV: "production",
    }
  }]
}