import os
import sys

# Add the project directory to the sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from flask import Flask
from flask_caching import Cache
# Initialize the Cache object globally without passing the app
cache = Cache()

from api.mlb.routes import mlb_schedule_bp
from home_routes import home_bp

def create_app():
    app = Flask(__name__)

    # Configure Flask-Caching to use Redis
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_HOST'] = 'redis-11688.c62.us-east-1-4.ec2.redns.redis-cloud.com'
    app.config['CACHE_REDIS_PORT'] = 11688
    app.config['CACHE_REDIS_PASSWORD'] = '8Iuw40BVrJ8JcX6Z2sXOfpZhWxEFj3cz'
    app.config['CACHE_REDIS_DB'] = 0
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Default cache timeout (5 minutes)

    # Initialize cache with the app
    cache.init_app(app)
    print(cache)
    # Home page
    app.register_blueprint(home_bp, url_prefix='/')

    app.register_blueprint(mlb_schedule_bp, url_prefix='/mlb')

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)