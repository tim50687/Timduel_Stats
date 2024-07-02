import json
from datetime import datetime
import pytz

class ScheduleProcessor:
    @staticmethod
    def save_schedule(data, filename="data/mlb_schedule.json"):
        with open(filename, "w") as f:
            # Save the data to a JSON file, set the indent to 4 for better readability
            json.dump(data, f, indent = 4)
    
    @staticmethod
    def extract_game_info(data):
        games = data.get("dates", [])[0].get("games", [])
        game_info_list = []
        est = pytz.timezone('US/Eastern')
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
            game_info_list.append(game_info)
        return game_info_list
    
    @staticmethod
    def convert_utc_to_est(utc_time_str):
        est = pytz.timezone('US/Eastern')
        # Parse the UTC time string to a datatime object
        utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
        # Set the timezone information for naive datetime object
        utc_time = pytz.utc.localize(utc_time)
        # Convert to EST
        est_time = utc_time.astimezone(est)

        return est_time.strftime("EST %H:%M")