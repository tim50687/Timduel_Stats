from flask import Blueprint, render_template, jsonify, request
from api.mlb.data_processing.odds_process import OddsProcessor
from api.mlb.data_processing.stats_process import PlayerStatsProcessor
from datetime import datetime  # Import datetime to handle date formatting
from api.mlb.s3_utils import get_object
import json

# Define the Blueprint for the MLB schedule
mlb_schedule_bp = Blueprint('mlb_schedule', __name__, template_folder='templates', static_folder='static')

BUCKET_NAME = 'timjimmymlbdata'
SCHEDULE_KEY = 'mlb_schedule.json'
ODDS_KEY = 'mlb_odds.json'
STATCAST_KEY = 'fangraphs_barrel_hh_data.json'
STATS_KEY = 'fangraphs_fb_data.json'

@mlb_schedule_bp.route('/schedule', methods=['GET'])
def show_schedule():
    """
    Route to display the MLB schedule.

    This route fetches the schedule data from s3 bucket.
    Returns:
        Rendered HTML template for the schedule page.
    """
    try:
        # Get the schedule from s3 bucket
        s3_response = get_object(BUCKET_NAME, SCHEDULE_KEY).decode('utf-8')
        games = json.loads(s3_response)

        # Get today's date and format it
        today_date = datetime.now().strftime("%A, %B %d, %Y")

        return render_template('schedule.html', schedule=games, today_date=today_date)
    except Exception as e:
        render_template('error.html', message=str(e))

    

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
        # Get the game id (api's game id) from the request parameters
        game_id = request.args.get('game_id')
        if not game_id:
            # Redirect to error page if game_id is not provided
            print("No game_id provided")
            return render_template('error.html')

        # Load odds data from s3 bucket
        s3_response = get_object(BUCKET_NAME, ODDS_KEY).decode('utf-8')
        odds_data = json.loads(s3_response)['entries']
        if odds_data is None:
            print("No odds data found")
            return render_template('error.html')
        
        game_odds_entries = []
        # Gather odds from different times for the game
        for entry in odds_data:
            if game_id in entry['data']:
                game_odds_entries.append(entry['data'][game_id])
                # Set the timestamp for the current entry
                game_odds_entries[-1]['timestamp'] = entry['timestamp']
        if not game_odds_entries:
            return render_template('error.html')
        
        # Process each entry (odds from different times)
        processed_entries = []
        for entry in game_odds_entries:
            processed_odds_data = OddsProcessor.sort_homerun_odd_by_booker(entry)
            processed_entries.append({
                'timestamp': entry['timestamp'], # Time that the odds were fetched
                'odds_data': processed_odds_data
            })

        # Get today's date and format it
        today_date = datetime.now().strftime("%A, %B %d, %Y")

        return render_template('odds.html', events=processed_entries, today_date=today_date)
    except Exception as e:
        # Return a JSON error message if an exception occurs
        return jsonify({'error': str(e)})
    

@mlb_schedule_bp.route('/player_stats', methods=['GET'])
def show_player_stats():
    """
    Route to display player stats for two teams.
    
    This route fetches player stats from the provided JSON files and displays them.
    
    Returns:
        Rendered HTML template for the player stats page.
    """
    try:
        # Get the team names from the request parameters
        team1 = request.args.get('team1')
        team2 = request.args.get('team2')
        
        if not team1 or not team2:
            return render_template('error.html', message="Both team1 and team2 parameters are required.")

        # File paths for the JSON data
        statcast_s3_response = get_object(BUCKET_NAME, STATCAST_KEY).decode('utf-8')
        stats_s3_response = get_object(BUCKET_NAME, STATS_KEY).decode('utf-8')
        statcast_file = json.loads(statcast_s3_response)
        stats_file = json.loads(stats_s3_response)
        
        # Get the complete player stats data
        complete_data = PlayerStatsProcessor.get_complete_data(statcast_file, stats_file)

        # Filter the data for the selected teams
        team1_stats = complete_data.get(team1)
        team2_stats = complete_data.get(team2)

        # Get today's date and format it
        today_date = datetime.now().strftime("%A, %B %d, %Y")

        return render_template('player_stats.html', team1=team1_stats, team2=team2_stats, team1_name=team1, team2_name=team2, today_date=today_date)
    
    except Exception as e:
        return render_template('error.html', message=str(e))
    
@mlb_schedule_bp.route('/hr_prediction', methods=['GET'])
def show_hr_prediction():
    """
    Route to display the home run prediction for a player.
    
    This route fetches the player stats from the provided JSON files and displays the home run prediction.
    
    Returns:
        Rendered HTML template for the home run prediction page.
    """
    try:
        # Define the key for the home run prediction data in S3
        HR_PREDICTION_KEY = 'hr_prediction_data.json'

        # Get prediction data from the S3 bucket
        s3_response = get_object(BUCKET_NAME, HR_PREDICTION_KEY).decode('utf-8')
        prediction_data = json.loads(s3_response)

        # Extract relevant fields (batter_id, predicted_home_runs, and team)
        hr_predictions = []
        for record in prediction_data:
            hr_predictions.append({
                'batter_id': record['batter_id'],
                'predicted_home_runs': record['predicted_homerun'],
                'team': record['team']
            })

        # Get today's date and format it
        today_date = datetime.now().strftime("%A, %B %d, %Y")

        # Render the hr_prediction.html template with the prediction data
        return render_template('hr_prediction.html', predictions=hr_predictions, today_date=today_date)
    
    except Exception as e:
        return render_template('error.html', message=str(e))