import json
from datetime import datetime, timezone
from app.mlb.mlb_schedule.external_apis.odds_api import fetch_events
from app.mlb.mlb_schedule.external_apis.schedule_api import MLBAPI
import pytz
import os

class ScheduleProcessor:
    @staticmethod
    def save_schedule(data, filename="data/mlb_schedule.json"):
        """
        Save the given data to a JSON file.

        Args:
            data (dict): The data to save.
            filename (str): The filename where the data should be saved.
        """
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    
    @staticmethod
    def extract_game_info(data):
        """
        Extracts game information from the given data and matches it with events fetched from the odds API.

        Args:
            data (dict): The data containing game information.

        Returns:
            list: A list of dictionaries with game information.
        """
        games = data.get("dates", [])[0].get("games", [])
        game_info_list = []

        # Get the events from odds api in order to get extract id
        events = fetch_events()
        
        # extract each game's information
        for game in games:
            game_time_est = ScheduleProcessor.convert_utc_to_est(game['gameDate'])
            game_info = {
                'date': game["gameDate"],
                'time': game_time_est,
                'away_team': game["teams"]["away"]["team"]["name"],
                'home_team': game["teams"]["home"]["team"]["name"], 
                'venue': game["venue"]["name"],
            }
            # Extract game id from api and add to game_info
            for event in events:
                if event['home_team'].lower() == game_info['home_team'].lower():
                    game_info['id'] = event['id']

            game_info_list.append(game_info)
        return game_info_list
    
    @staticmethod
    def convert_utc_to_est(utc_time_str):
        """
        Converts a UTC time string to EST time string.

        Args:
            utc_time_str (str): The UTC time string in ISO 8601 format.

        Returns:
            str: The converted EST time string.
        """
        est = pytz.timezone('US/Eastern')

        # Parse the UTC time string to a datatime object
        utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')

        # Set the timezone information for naive datetime object
        utc_time = pytz.utc.localize(utc_time)
        
        # Convert to EST
        est_time = utc_time.astimezone(est)

        return est_time.strftime("EST %H:%M")

    @staticmethod
    def get_or_fetch_schedule(file_path="data/mlb_schedule.json"):
        """
        Get the schedule data from a JSON file if it exists and is from today,
        otherwise fetch it from the API and save it to the file.

        Args:
            file_path (str): The path to the schedule JSON file.

        Returns:
            dict: The schedule data.
        """
        est = pytz.timezone('US/Eastern')
        now_est = datetime.now(est)

        # Check if the schedule file exists and is not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path), tz=est)
            file_date = file_mtime.date()
            today_date = now_est.date()
            
            if file_date == today_date:
                # Read the schedule data from the file
                with open(file_path, "r") as f:
                    return json.load(f)
        
        # Fetch the schedule using MLBAPI
        data = MLBAPI.get_schedule()
        # Save the schedule data to the file
        ScheduleProcessor.save_schedule(data)
        print("fetch new")
        return data