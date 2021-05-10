module.exports = {
    apps : [{
      name: "Live Data Service",
      script: "./live_data_service.js",
      env: {
        NODE_ENV: "development",
        POSTGRES_SERVICES_DB_USER: "live_data_service",
      },
      env_production: {
        NODE_ENV: "production",
        POSTGRES_SERVICES_DB_USER: "live_data_service",
      }
    }]
  }