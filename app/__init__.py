from flask import Flask
from app.mlb.mlb_schedule.routes import mlb_schedule_bp
from apscheduler.schedulers.background import BackgroundScheduler
from app.mlb.mlb_schedule.utils.odds_utils import fetch_and_save_homerun_odds
import os

def create_app():
    app = Flask(__name__)

    app.register_blueprint(mlb_schedule_bp, url_prefix='/mlb')

    # Function to fetch and save homerun odds
    def scheduled_task():
        print("Fetching and saving homerun odds...")
        fetch_and_save_homerun_odds()

    # Set up APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=scheduled_task, trigger='interval', hours=2)

    # Conditionally run the task once when the app starts
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        scheduled_task()  # Run the task once when the app starts
        scheduler.start()  # Start the scheduler

    return app

