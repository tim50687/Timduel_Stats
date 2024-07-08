import requests
from datetime import datetime, timezone, timedelta
import pytz

class MLBAPI:
    BASE_URL = 'https://statsapi.mlb.com/api/v1/'

    @staticmethod
    def get_current_est_date():
        """
        Get the current date in EST.

        Returns:
            str: The current date in EST in YYYY-MM-DD format.
        """
        est = pytz.timezone('US/Eastern')
        now_est = datetime.now(est)
        return now_est.strftime('%Y-%m-%d')

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
        current_date = MLBAPI.get_current_est_date()
        url = f"{MLBAPI.BASE_URL}/schedule/games/?sportId={sport_id}&startDate={current_date}&endDate={current_date}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()