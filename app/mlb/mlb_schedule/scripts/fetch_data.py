from app.mlb.mlb_schedule.api import MLBAPI
from app.mlb.mlb_schedule.schedule import ScheduleProcessor

def main():
    # Get the schedule for MLB
    schedules = MLBAPI.get_schedule()
    # Extract game information
    game_info_list = ScheduleProcessor.extract_game_info(schedules)

    for game_info in game_info_list:
        print(f"Date: {game_info['date']}")
        print(f"Away Team: {game_info['away_team']}")
        print(f"Home Team: {game_info['home_team']}")
        print(f"Venue: {game_info['venue']}")
        print('-' * 40)

    # Save the data
    ScheduleProcessor.save_schedule(schedules)

if __name__ == "__main__":
    main()