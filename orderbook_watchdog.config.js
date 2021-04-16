module.exports = {
    apps : [{
      name: "Orderbook WatchDog",
      script: "python3 -u orderbook_watchdog.py",
      env: {
        NODE_ENV: "development",
      },
      env_production: {
        NODE_ENV: "production",
      }
    }]
  }