module.exports = {
  apps : [{
    name: "Orderbook FTX BTC-PERP",
    script: "python3 -u $HOME/code/obook/orderbook_feeder.py FTX \"BTC-PERP\"",
    time: true,
    env: {
      NODE_ENV: "development",
    },
    env_production: {
      NODE_ENV: "production",
    }
  }]
}