import requests

class MLBAPI:
    BASE_URL = 'https://statsapi.mlb.com/api/v1/'

    @staticmethod
    def get_schedule(sport_id=1):
        """
        Fetches the schedule for the specified sport.

        Args:
            sport_id (int): The ID of the sport. Defaults to 1 for MLB.

        Returns:
            dict: The JSON response containing the schedule data.

        Raises:
            requests.exceptions.RequestException: If the request fails or returns a bad status code.
        """
        url = f"{MLBAPI.BASE_URL}/schedule/games/?sportId={sport_id}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()