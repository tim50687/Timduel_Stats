import requests
from .config import API_KEY, SPORT, REGIONS, MARKETS, ODDS_FORMAT, DATE_FORMAT


def fetch_events():
    response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/events',
        params={
            'apiKey' : API_KEY,
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

