from datetime import datetime, timedelta, timezone

def get_utc_start_and_end():
    """
    Get the start and end of the current UTC day. If the current time is after midnight UTC, 
    adjust to the previous day.
    """
    now_utc = datetime.now(timezone.utc)

    if now_utc.hour >= 0 and now_utc.hour < 3:
        start_of_today_utc = now_utc - timedelta(days=1)
    else:
        start_of_today_utc = now_utc

    start_of_today_utc = start_of_today_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_tomorrow_utc = start_of_today_utc + timedelta(days=1) + timedelta(hours=2)

    return start_of_today_utc.strftime('%Y-%m-%dT%H:%M:%SZ'), start_of_tomorrow_utc.strftime('%Y-%m-%dT%H:%M:%SZ')