module.exports = {
    apps : [{
      name: "Live Data Service",
      script: "./live_data_service.js",
      env: {
        NODE_ENV: "development",
      },
      env_production: {
        NODE_ENV: "production",
      }
    }]
  }