from datetime import datetime, timedelta, timezone

def get_utc_start_and_end():
    """
    Get the UTC start and end times for the current day. If the current time is between midnight 
    and 3 AM UTC, adjust the range to cover the previous day.

    Returns:
        tuple: A tuple containing the start and end times in ISO 8601 format.
    """
    # Get the current UTC time
    now_utc = datetime.now(timezone.utc)

    # If the current time is between midnight and 3 AM UTC, adjust to the previous day
    if 0 <= now_utc.hour < 3:
        # Set the start of the day to the previous day
        start_of_today_utc = now_utc - timedelta(days=1)
    else:
        # Otherwise, set the start of the day to today
        start_of_today_utc = now_utc

    # Reset the time to midnight of the start day
    start_of_today_utc = start_of_today_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Set the end time to 2 AM of the next day
    end_of_today_utc = start_of_today_utc + timedelta(days=1, hours=2)

    # Convert the times to ISO 8601 format
    today_str = start_of_today_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_str = end_of_today_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

    return today_str, end_str