import json
import os
from datetime import datetime, timedelta
from app.mlb.mlb_schedule.external_apis.odds_api import fetch_homerun_odds
from app.mlb.mlb_schedule.external_apis.odds_api import fetch_events

# TODO: Fix the path to the JSON file
JSON_FILE_PATH = '../../../../data/odds_data.json'

def fetch_and_save_homerun_odds():
    """
    Fetches homerun odds from the API for a list of game IDs and saves it to a JSON file.

    Args:
        game_ids (list): The list of game IDs to fetch the odds for.

    Returns:
        dict: The combined odds data fetched from the API.
    """
    # Get all the events for today
    # TODO: Can call fetch events once per day and store the data in a file
    events = fetch_events()
    game_ids = [event['id'] for event in events]

    # Load existing data if available
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = {'entries': []}

    combined_odds_data = {}
    for game_id in game_ids:
        odds_data = fetch_homerun_odds(game_id)
        combined_odds_data[game_id] = odds_data

    # Add new entry with timestamp
    new_entry = {
        'timestamp': datetime.now().isoformat(),
        'data': combined_odds_data
    }
    existing_data['entries'].append(new_entry)

    # Save updated data
    with open(JSON_FILE_PATH, 'w') as json_file:
        json.dump(existing_data, json_file)

    return combined_odds_data

def load_odds_from_json():
    """
    Loads the odds data from the JSON file if it exists.

    Returns:
        dict: The odds data from the JSON file, or None if the file doesn't exist.
    """
    if not os.path.exists(JSON_FILE_PATH):
        return None
    
    with open(JSON_FILE_PATH, 'r') as json_file:
        data = json.load(json_file)
    
    return data['entries']

if __name__ == "__main__":
    fetch_and_save_homerun_odds()
    print(load_odds_from_json())