module.exports = {
  apps : [{
    name: "Orderbook FTX ETH-PERP",
    script: "python3 -u orderbook_feeder.py FTX \"ETH-PERP\"",
    env: {
      NODE_ENV: "development",
    },
    env_production: {
      NODE_ENV: "production",
    }
  }]
}