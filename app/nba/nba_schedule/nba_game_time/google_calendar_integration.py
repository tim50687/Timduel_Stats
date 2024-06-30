from pprint import pprint
from google_apis import create_service
from datetime import datetime, timedelta
import json

# Define the Google Calendar API credentials
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPE = ['https://www.googleapis.com/auth/calendar']

# Create a Google Calendar API service
service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPE)


def create_calendar():
    request = {
        'summary': 'NBA Tip Off Tracker',
    }
    response = service.calendars().insert(body=request).execute()
    return response


def create_events(response):

    # Load JSON data from the taday_match.json file
    with open("today_match.json", "r") as f:
        games = json.load(f)

    for game in games:
        # Extract game information
        game_date_time_est = game["game_date_time_est"][:-1]
        arena_city = game["arena_city"]
        arena_state = game["arena_state"]
        arena_name = game["arena_name"]
        home_team = game["home_team"]
        away_team = game["away_team"]

        # Parse game date and time
        game_datetime_est = datetime.fromisoformat(game_date_time_est)
        # Calculate end time by adding 2 hours to the start time
        end_time_est = game_datetime_est + timedelta(hours=2)
        end_time_str = end_time_est.isoformat()

        # Define the event request body
        event_request_body = {
            'start': {
                'dateTime': game_date_time_est,
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end_time_str,
                'timeZone': 'America/New_York',
            },
            'summary': f'{away_team} vs {home_team}',
            'description': f'NBA Game: {away_team} vs. {home_team} at {arena_name}, {arena_city}, {arena_state}',
            'status': 'confirmed',
            'location': f'{arena_name}, {arena_city}, {arena_state}',
            # Indicates that the event can overlap with other events
            'transparency': 'transparent',

        }
        # Insert the event into the calendar
        service.events().insert(
            calendarId=response['id'],
            sendUpdates='all',
            body=event_request_body
        ).execute()


if __name__ == '__main__':
    # To do:
    # Remove the old calendar

    # Create a calendar
    response = create_calendar()
    # Create events
    create_events(response)
