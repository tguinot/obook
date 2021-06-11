module.exports = {
  apps : [{
    name: "Orderbook FTX XRP-PERP",
    script: "python3 -u orderbook_feeder.py FTX \"XRP-PERP\"",
    time: true,
    env: {
      NODE_ENV: "development",
    },
    env_production: {
      NODE_ENV: "production",
    }
  }]
}