module.exports = {
  apps : [{
    name: "Orderbook FTX BTC/USD",
    script: "python3 -u orderbook_feeder.py FTX \"BTC/USD\"",
    time: true,
    env: {
      NODE_ENV: "development",
    },
    env_production: {
      NODE_ENV: "production",
    }
  }]
}