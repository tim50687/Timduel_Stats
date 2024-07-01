from flask import Blueprint, render_template
from app.mlb.mlb_schedule.api import MLBAPI
from app.mlb.mlb_schedule.schedule import ScheduleProcessor
from datetime import datetime  # Import datetime to handle date formatting

mlb_schedule_bp = Blueprint('mlb_schedule', __name__, template_folder='templates', static_folder='static')


@mlb_schedule_bp.route('/schedule', methods=['GET'])
def show_schedule():
    # Fetch the schedule using MLBAPI
    data = MLBAPI.get_schedule()

    # Process the schedule data
    games = ScheduleProcessor.extract_game_info(data)

    # Save the schedule data
    ScheduleProcessor.save_schedule(data)

    # Get today's date and format it
    today_date = datetime.now().strftime("%A, %B %d, %Y")

    return render_template('schedule.html', schedule=games, today_date=today_date)