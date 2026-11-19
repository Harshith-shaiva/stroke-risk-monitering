# run.py
# Development entry point.
# Usage:  python run.py
#         FLASK_ENV=production python run.py

import os
from app import create_app

env = os.getenv("FLASK_ENV", "production")
config_map = {
    "development": "config.DevelopmentConfig",
    "testing":     "config.TestingConfig",
    "production":  "config.ProductionConfig",
}
config_object = config_map.get(env, "config.ProductionConfig")

app = create_app(config_object)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
