module.exports = {
  apps : [{
    name: "Orderbook FTX LTC-PERP",
    script: "python3 -u $HOME/code/obook/orderbook_feeder.py FTX \"LTC-PERP\"",
    time: true,
    env: {
      NODE_ENV: "development",
    },
    env_production: {
      NODE_ENV: "production",
    }
  }]
}