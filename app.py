import os
import sys

# Add the project directory to the sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

print(project_root)

from flask import Flask
from app.mlb.mlb_schedule.routes import mlb_schedule_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(mlb_schedule_bp, url_prefix='/mlb')

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)