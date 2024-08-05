from flask import Flask
from app.mlb.mlb_schedule.routes import mlb_schedule_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(mlb_schedule_bp, url_prefix='/mlb')

    return app

