module.exports = {
  apps : [{
    name: "Orderbook FTX BNB-PERP",
    script: "python3 -u orderbook_feeder.py FTX \"BNB-PERP\"",
    time: true,
    env: {
      NODE_ENV: "development",
    },
    env_production: {
      NODE_ENV: "production",
    }
  }]
}