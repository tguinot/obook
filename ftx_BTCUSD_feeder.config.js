module.exports = {
  apps : [{
    name: "Orderbook FTX BTC/USD",
    script: "python3 -u orderbook_feeder.py FTX \"BTC/USD\"",
    env: {
      NODE_ENV: "development",
    },
    env_production: {
      NODE_ENV: "production",
    }
  }]
}