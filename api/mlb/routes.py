from flask import Blueprint, render_template, jsonify, request, current_app
from api.mlb.data_processing.odds_process import OddsProcessor
from api.mlb.data_processing.stats_process import PlayerStatsProcessor
from datetime import datetime  # Import datetime to handle date formatting
from api.mlb.s3_utils import get_object
import json
from io import StringIO
import csv
import redis
from operator import itemgetter
# Define the Blueprint for the MLB schedule
mlb_schedule_bp = Blueprint('mlb_schedule', __name__, template_folder='templates', static_folder='static')

BUCKET_NAME = 'timjimmymlbdata'
SCHEDULE_KEY = 'mlb_schedule.json'
ODDS_KEY = 'mlb_odds.json'
STATCAST_KEY = 'fangraphs_barrel_hh_data.json'
STATS_KEY = 'fangraphs_fb_data.json'
HR_PREDICTION_KEY = 'predicted_homeruns2.csv'



@mlb_schedule_bp.route('/', methods=['GET'])
def show_schedule():
    """
    Route to display the MLB schedule with Redis caching.
    """
    try:
        # Connect to Redis
        redis_client = redis.StrictRedis(
            host='redis-11688.c62.us-east-1-4.ec2.redns.redis-cloud.com',  
            port=11688,  
            password='8Iuw40BVrJ8JcX6Z2sXOfpZhWxEFj3cz',  
            db=0
        )

        # Check if the schedule is already cached
        cached_schedule = redis_client.get('mlb_schedule')
        if cached_schedule:
            # Return cached data
            games = json.loads(cached_schedule)
            print("Cache hit: Returning schedule from Redis")
        else:
            # If not cached, fetch from S3
            s3_response = get_object(BUCKET_NAME, SCHEDULE_KEY).decode('utf-8')
            games = json.loads(s3_response)

            # Store the result in Redis
            redis_client.setex('mlb_schedule', 300, json.dumps(games))
            print("Cache miss: Fetched schedule from S3 and stored in Redis")

        today_date = datetime.now().strftime("%A, %B %d, %Y")
        return render_template('schedule.html', schedule=games, today_date=today_date)

    except Exception as e:
        return render_template('error.html', message=str(e))

    

# @mlb_schedule_bp.route('/odds', methods=['GET'])
# def get_odds():
#     """
#     Route to display the homerun odds for a specific game using Redis caching.
#     """
#     try:
#         # Get the game id (api's game id) from the request parameters
#         game_id = request.args.get('game_id')
#         if not game_id:
#             # Redirect to error page if game_id is not provided
#             print("No game_id provided")
#             return render_template('error.html')
        
#         # Initialize Redis client
#         redis_client = redis.StrictRedis(
#             host='redis-11688.c62.us-east-1-4.ec2.redns.redis-cloud.com',  
#             port=11688,  
#             password='8Iuw40BVrJ8JcX6Z2sXOfpZhWxEFj3cz',  
#             db=0
#             )
#         # Try to get the odds from Redis cache
#         cached_odds = redis_client.get(f'game_odds_{game_id}')
#         if cached_odds:
#             # If found in cache, load from Redis and return it
#             print("Cache hit: Returning odds from Redis")
#             game_odds_entries = json.loads(cached_odds)
#         else:
#             # Load odds data from s3 bucket
#             s3_response = get_object(BUCKET_NAME, ODDS_KEY).decode('utf-8')
#             odds_data = json.loads(s3_response)['entries']
#             if odds_data is None:
#                 print("No odds data found")
#                 return render_template('error.html')
            
#             game_odds_entries = []
#             # Gather odds from different times for the game
#             for entry in odds_data:
#                 if game_id in entry['data']:
#                     game_odds_entries.append(entry['data'][game_id])
#                     # Set the timestamp for the current entry
#                     game_odds_entries[-1]['timestamp'] = entry['timestamp']
            
#             redis_client.setex(f'game_odds_{game_id}', 300, json.dumps(game_odds_entries))

#         if not game_odds_entries:
#             return render_template('error.html')
        
#         # Process each entry (odds from different times)
#         processed_entries = []
#         for entry in game_odds_entries:
#             processed_odds_data = OddsProcessor.sort_homerun_odd_by_booker(entry)
#             processed_entries.append({
#                 'timestamp': entry['timestamp'], # Time that the odds were fetched
#                 'odds_data': processed_odds_data
#             })

#         # Get today's date and format it
#         today_date = datetime.now().strftime("%A, %B %d, %Y")

#         return render_template('odds.html', events=processed_entries, today_date=today_date)
#     except Exception as e:
#         # Return a JSON error message if an exception occurs
#         return jsonify({'error': str(e)})
    

@mlb_schedule_bp.route('/player_stats', methods=['GET'])
def show_player_stats():
    """
    Route to display player stats for two teams using Redis caching.
    """
    try:
        # Get the team names from the request parameters
        team1 = request.args.get('team1')
        team2 = request.args.get('team2')
        
        if not team1 or not team2:
            return render_template('error.html', message="Both team1 and team2 parameters are required.")

        # Initialize Redis client
        redis_client = redis.StrictRedis(
            host='redis-11688.c62.us-east-1-4.ec2.redns.redis-cloud.com',  
            port=11688,  
            password='8Iuw40BVrJ8JcX6Z2sXOfpZhWxEFj3cz',  
            db=0
            )

        # Generate a cache key based on the teams
        cache_key = f'player_stats_{team1}_{team2}'

        # Check if the player stats are already cached in Redis
        cached_stats = redis_client.get(cache_key)
        if cached_stats:
            print("Cache hit: Returning player stats from Redis")
            player_stats = json.loads(cached_stats)
        else:
            print("Cache miss: Fetching player stats from S3")

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

            # Combine the stats for caching
            player_stats = {
                'team1_stats': team1_stats,
                'team2_stats': team2_stats
            }

            # Cache the player stats in Redis for 1 hour
            redis_client.setex(cache_key, 300, json.dumps(player_stats))

        # Get today's date and format it
        today_date = datetime.now().strftime("%A, %B %d, %Y")

        return render_template('player_stats.html', team1=player_stats['team1_stats'], 
                               team2=player_stats['team2_stats'], 
                               team1_name=team1, team2_name=team2, today_date=today_date)
    
    except Exception as e:
        return render_template('error.html', message=str(e))
    
@mlb_schedule_bp.route('/hr_prediction', methods=['GET'])  
def show_hr_prediction():
    """
    Route to display the home run prediction for a player using Redis caching.
    """
    try:
        # Initialize Redis client
        redis_client = redis.StrictRedis(
            host='redis-11688.c62.us-east-1-4.ec2.redns.redis-cloud.com',  
            port=11688,  
            password='8Iuw40BVrJ8JcX6Z2sXOfpZhWxEFj3cz',  
            db=0
            )

        # Cache key for home run prediction
        cache_key = 'hr_prediction'

        # Check if home run predictions are already cached
        cached_predictions = redis_client.get(cache_key)
        if cached_predictions:
            print("Cache hit: Returning home run predictions from Redis")
            hr_predictions = json.loads(cached_predictions)
        else:
            print("Cache miss: Fetching home run predictions from S3")

            # Get prediction data from the S3 bucket
            s3_response = get_object(BUCKET_NAME, HR_PREDICTION_KEY).decode('utf-8')

            # Use StringIO to read the CSV data into a format that the csv module can handle
            csv_file = StringIO(s3_response)
            reader = csv.DictReader(csv_file)

            # Extract relevant fields (batter_id, predicted_home_runs, and team)
            hr_predictions = []
            for record in reader:
                hr_predictions.append({
                    'batter_id': record['batter_id'],
                    'predicted_home_runs': record['predicted_homerun'],
                    'team': record['team']
                })

            # Cache the predictions in Redis for 1 hour
            redis_client.setex(cache_key, 300, json.dumps(hr_predictions))

        # Sort predictions by team before passing them to the template
        hr_predictions_sorted = sorted(hr_predictions, key=itemgetter('team'))

        # Get today's date and format it
        today_date = datetime.now().strftime("%A, %B %d, %Y")

        # Render the hr_prediction.html template with the prediction data
        return render_template('hr_prediction.html', predictions=hr_predictions_sorted, today_date=today_date)
    
    except Exception as e:
        return render_template('error.html', message=str(e))
