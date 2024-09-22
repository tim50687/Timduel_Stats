import os
import sys

# Add the project directory to the sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

print(project_root)

from flask import Flask
from api.mlb.routes import mlb_schedule_bp
from home_routes import home_bp

def create_app():
    app = Flask(__name__)

    # Home page
    app.register_blueprint(home_bp, url_prefix='/')

    app.register_blueprint(mlb_schedule_bp, url_prefix='/mlb')

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)