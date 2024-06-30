import json

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
        # extract each game's information
        for game in games:
            game_info = {
                'date': game["gameDate"],
                'away_team': game["teams"]["away"]["team"]["name"],
                'home_team': game["teams"]["home"]["team"]["name"], 
                'venue': game["venue"]["name"],
            }
            game_info_list.append(game_info)
        return game_info_list