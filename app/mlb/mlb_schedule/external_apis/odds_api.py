import requests
from datetime import datetime, timedelta, timezone
from .config import API_KEY, SPORT, REGIONS, MARKETS, ODDS_FORMAT, DATE_FORMAT
from .datetime_helpers import get_utc_start_and_end

def fetch_events():
    """
    Fetch today's MLB events using the Odds API.
    """
    today_str, tomorrow_str = get_utc_start_and_end()

    response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/events',
        params={
            'apiKey' : API_KEY,
            'commenceTimeFrom': today_str,
            'commenceTimeTo': tomorrow_str,
            'dateFormat': 'iso'
        }
    )

    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch odds: {response.status_code}, {response.text}")

    return response.json()

def fetch_homerun_odds(event_id):
    response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/events/{event_id}/odds',
        params={
            'apiKey' : API_KEY,
            'regions' : REGIONS,
            'markets' : MARKETS,
            'oddsFormat' : ODDS_FORMAT,
            'dateFormat' : DATE_FORMAT
        }
    )

    if response.status_code != 200:
        raise Exception(f"Failed to fetch odds: {response.status_code}, {response.text}")

    return response.json()

