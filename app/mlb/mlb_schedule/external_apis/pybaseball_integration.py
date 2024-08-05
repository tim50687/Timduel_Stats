import pybaseball
from pybaseball import statcast_batter, statcast_batter, playerid_reverse_lookup
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


