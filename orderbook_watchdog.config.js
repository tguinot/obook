module.exports = {
    apps : [{
      name: "Orderbook WatchDog",
      script: "python3 -u orderbook_watchdog.py",
      env: {
        NODE_ENV: "development",
        POSTGRES_SERVICES_DB_USER: "watchdog",
      },
      env_production: {
        NODE_ENV: "production",
        POSTGRES_SERVICES_DB_USER: "watchdog",
      }
    }]
  }