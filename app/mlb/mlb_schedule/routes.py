from flask import Blueprint, render_template, jsonify, request
from app.mlb.mlb_schedule.schedule_api import MLBAPI
from app.mlb.mlb_schedule.odds_api import fetch_homerun_odds
from app.mlb.mlb_schedule.schedule_process import ScheduleProcessor
from app.mlb.mlb_schedule.odds_process import OddsProcessor
from datetime import datetime  # Import datetime to handle date formatting
import json

# Define the Blueprint for the MLB schedule
mlb_schedule_bp = Blueprint('mlb_schedule', __name__, template_folder='templates', static_folder='static')


@mlb_schedule_bp.route('/schedule', methods=['GET'])
def show_schedule():
    """
    Route to display the MLB schedule.

    This route fetches the schedule data using the MLBAPI class, processes the data using the
    ScheduleProcessor class, saves the schedule, and then renders the schedule.html template.

    Returns:
        Rendered HTML template for the schedule page.
    """
     # Get the schedule data, either from file or API
    data = ScheduleProcessor.get_or_fetch_schedule()

    # Process the schedule data
    games = ScheduleProcessor.extract_game_info(data)

    # Save the schedule data
    ScheduleProcessor.save_schedule(data)

    # Get today's date and format it
    today_date = datetime.now().strftime("%A, %B %d, %Y")

    return render_template('schedule.html', schedule=games, today_date=today_date)

@mlb_schedule_bp.route('/odds', methods=['GET'])
def get_odds():
    """
    Route to display the homerun odds for a specific game.

    This route fetches the homerun odds for the specified game ID, processes the odds data using the
    OddsProcessor class, and then renders the odds.html template. If the game ID is not provided,
    it redirects to an error page.

    Returns:
        Rendered HTML template for the odds page or JSON error message.
    """
    try:
        # Get the game id from the request parameters
        game_id = request.args.get('game_id')
        if not game_id:
            # Redirect to error page if game_id is not provided
            return render_template('error.html')

        # Fetch the homerun odds using the game ID
        odds_data = fetch_homerun_odds(game_id)
        # Process the odds data to sort it by bookmaker
        processed_odds_data = OddsProcessor.sort_homerun_odd_by_booker(odds_data)

        # Get today's date and format it
        today_date = datetime.now().strftime("%A, %B %d, %Y")

        return render_template('odds.html', events=processed_odds_data, today_date=today_date)
    except Exception as e:
        # Return a JSON error message if an exception occurs
        return jsonify({'error': str(e)})
    

@mlb_schedule_bp.route('/player_stats', methods=['GET'])
def show_player_stats():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    if not team1 or not team2:
        return render_template('error.html')

    # Get player stats
    combined_data = PlayerStatsProcessor.combine_player_stats(barrel_hh_data, fb_data)

    # Filter the data for the specified teams
    team1_stats = combined_data.get(team1, {})
    team2_stats = combined_data.get(team2, {})

    return render_template('player_stats.html', team1=team1, team2=team2, team1_stats=team1_stats, team2_stats=team2_stats)