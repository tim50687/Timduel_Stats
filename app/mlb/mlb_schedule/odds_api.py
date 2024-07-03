import requests
from datetime import datetime, timedelta
from .config import API_KEY, SPORT, REGIONS, MARKETS, ODDS_FORMAT, DATE_FORMAT


def fetch_events():
    # Get today's date in ISO 8601 format
    today = datetime.utcnow()
    tomorrow = today + timedelta(days=1)
    today_str = today.strftime('%Y-%m-%dT00:00:00Z')
    tomorrow_str = tomorrow.strftime('%Y-%m-%dT00:00:00Z')

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

