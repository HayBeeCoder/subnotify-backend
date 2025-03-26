from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+
# OR (for older Python versions)
# from pytz import timezone

class Subscription(BaseModel):
    provider: str
    type: str
    description: Optional[str] = Field(
        default=None, title="The description of the service subscribed to.",
    )
    start_date: int  # Unix timestamp in seconds
    end_date: int    # Unix timestamp in seconds
    user_timezone: str  # User's time zone, e.g., "America/New_York"
