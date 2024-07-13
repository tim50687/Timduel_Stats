from flask import Blueprint, render_template, jsonify, request
from app.mlb.mlb_schedule.external_apis.schedule_api import MLBAPI
from app.mlb.mlb_schedule.external_apis.odds_api import fetch_homerun_odds
from app.mlb.mlb_schedule.data_processing.schedule_process import ScheduleProcessor
from app.mlb.mlb_schedule.data_processing.odds_process import OddsProcessor
from app.mlb.mlb_schedule.data_processing.stats_process import PlayerStatsProcessor
from datetime import datetime  # Import datetime to handle date formatting


import pandas as pd # temporary

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
        statcast_file = "data/fangraphs_barrel_hh_data.json"
        stats_file = "data/fangraphs_fb_data.json"
        
        # Get the complete player stats data
        complete_data = PlayerStatsProcessor.get_complete_data(statcast_file, stats_file)

        # Filter the data for the selected teams
        team1_stats = complete_data.get(team1)
        team2_stats = complete_data.get(team2)

        # Get today's date and format it
        today_date = datetime.now().strftime("%A, %B %d, %Y")


        ### Save to Excel   ### temporary
        # save_to_excel(team1_stats, team2_stats, team1, team2)

        ###### 


        
        return render_template('player_stats.html', team1=team1_stats, team2=team2_stats, team1_name=team1, team2_name=team2, today_date=today_date)
    
    except Exception as e:
        return render_template('error.html', message=str(e))
    

def save_to_excel(team1_stats, team2_stats, team1_name, team2_name, file_name="team_stats.xlsx"):
    """
    Save the team stats to an Excel file.

    Args:
        team1_stats (dict): The stats data for the first team.
        team2_stats (dict): The stats data for the second team.
        team1_name (str): The name of the first team.
        team2_name (str): The name of the second team.
        file_name (str): The name of the Excel file to save the data.
    """
    # Convert the dictionaries to pandas DataFrames
    df_team1 = pd.DataFrame.from_dict(team1_stats, orient='index')
    df_team2 = pd.DataFrame.from_dict(team2_stats, orient='index')

    # Write the DataFrames to an Excel file
    with pd.ExcelWriter(file_name, mode='a') as writer:
        df_team1.to_excel(writer, sheet_name=team1_name)
        df_team2.to_excel(writer, sheet_name=team2_name)
    
    print(f"Data saved to {file_name}")