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
            game_time = datetime.strptime(game["gameDate"], "%Y-%m-%dT%H:%M:%SZ")
            game_time_est = game_time.astimezone(est).strftime("EST %H:%M")
            game_info = {
                'date': game["gameDate"],
                'time': game_time_est,
                'away_team': game["teams"]["away"]["team"]["name"],
                'home_team': game["teams"]["home"]["team"]["name"], 
                'venue': game["venue"]["name"],
            }
            game_info_list.append(game_info)
        return game_info_list