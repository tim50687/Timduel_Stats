import requests

class MLBAPI:
    BASE_URL = 'https://statsapi.mlb.com/api/v1/'

    # Define a static method to get the schedule
    @staticmethod
    def get_schedule(sport_id = 1):
        # Get the schedule for the specified sport
        url = f"{MLBAPI.BASE_URL}/schedule/games/?sportId={sport_id}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()