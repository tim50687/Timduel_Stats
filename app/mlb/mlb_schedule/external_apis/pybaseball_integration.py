import pybaseball
from pybaseball import playerid_lookup, statcast_batter, statcast, batting_stats_range, statcast_batter, playerid_reverse_lookup, get_splits
from datetime import datetime

def fetch_batter_statcast_data(start_date, end_date, player_id):
    """
    Fetch statcast data for a specific batter within a date range.

    Args:
        start_date (str): The start date in YYYY-MM-DD format.
        end_date (str): The end date in YYYY-MM-DD format.
        player_id (int): The player ID for the batter.

    Returns:
        DataFrame: Filtered statcast data with selected columns.
    """
    columns_to_keep = [
        'player_name', 'pitcher', 'description', 'bb_type', 'hit_distance_sc', 
        'launch_speed', 'launch_angle', 'pitch_name'
    ]
    
    # Fetch the data
    data = statcast_batter(start_date, end_date, player_id=player_id)
    
    # Select the desired columns
    filtered_data = data[columns_to_keep]
    # return data
    return filtered_data

def save_data_to_csv(data, filename):
    """
    Save the DataFrame to a CSV file.

    Args:
        data (DataFrame): The DataFrame to save.
        filename (str): The filename for the CSV file.
    """
    data.to_csv(filename, index=False)


if __name__ == "__main__":
    start_date = '2024-07-02'
    end_date = '2024-07-06'

    data = playerid_reverse_lookup([670174], key_type='mlbam')
    save_data_to_csv(data, 'data.csv')
    statcast_data = fetch_batter_statcast_data(start_date, end_date, 592450)


    save_data_to_csv(statcast_data, 'statcast_data.csv')
