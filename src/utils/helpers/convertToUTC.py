import datetime
import pytz

def convertToUTC(user_timestamp: float, user_timezone_str: str) -> int:
    """
    Converts a user timestamp (in seconds) to a UTC-based date string.
    
    Parameters:
    - user_timestamp: e.g., 1712899200.0 (seconds since epoch)
    - user_timezone_str: e.g., 'Africa/Lagos'

    Returns:
    - UTC date string (YYYY-MM-DD)
    """
    # Convert timestamp to naive datetime
    naive_datetime = datetime.datetime.fromtimestamp(user_timestamp)

    # Localize to user's timezone
    user_timezone = pytz.timezone(user_timezone_str)
    localized_datetime = user_timezone.localize(naive_datetime)

    # Convert to UTC
    utc_datetime = localized_datetime.astimezone(pytz.utc)

    # Truncate to start of UTC day
    utc_date_start = datetime.datetime.combine(utc_datetime.date(), datetime.time(0, 0), tzinfo=pytz.utc)

    # Return as timestamp (in seconds)
    return int(utc_date_start.timestamp())

