from flask import Blueprint, render_template, jsonify, request
from app.mlb.mlb_schedule.schedule_api import MLBAPI
from app.mlb.mlb_schedule.odds_api import fetch_events, fetch_homerun_odds
from app.mlb.mlb_schedule.schedule import ScheduleProcessor
from app.mlb.mlb_schedule.odds_process import OddsProcessor
from datetime import datetime  # Import datetime to handle date formatting
import json

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

# Get the homerun odds
@mlb_schedule_bp.route('/odds', methods=['GET'])
def get_odds():
    try:
        # Get the game id 
        game_id = request.args.get('game_id')
        if not game_id:
            # Redirect to error page
            return render_template('error.html')

        odds_data = fetch_homerun_odds(game_id)
        processed_odds_data = OddsProcessor.sort_homerun_odd_by_booker(odds_data)

        # Get today's date and format it
        today_date = datetime.now().strftime("%A, %B %d, %Y")

        return render_template('odds.html', events=processed_odds_data, today_date=today_date)
    except Exception as e:
        return jsonify({'error' : str(e)})