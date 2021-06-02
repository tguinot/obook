module.exports = {
  apps : [{
    name: "Orderbook FTX BTC-PERP",
    script: "python3 -u orderbook_feeder.py FTX \"BTC-PERP\"",
    env: {
      NODE_ENV: "development",
    },
    env_production: {
      NODE_ENV: "production",
    }
  }]
}