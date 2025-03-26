from pydantic import BaseModel, Field, field_validator
from typing import Optional
import pytz
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
    
    @field_validator("user_timezone")
    def ensure_valid_user_timezone(cls, value: str):
        if value in pytz.all_timezones:
            return value
        else:
            raise ValueError(f"{value} is not a valid timezone!")
    class Config:
        json_schema_extra = {
            "example": {
                "provider": "Netflix",
                "type": "Streaming",
                "description": "Monthly subscription for Netflix Premium",
                "start_date": 1711824000,  
                "end_date": 1714502400,  
                "user_timezone": "America/New_York"
            }
        }
        

class SubscriptionsResponse(BaseModel):
    provider: str
    type: str
    description: str
    start_date: str
    end_date: str
    user_timezone: str
    
    class Config:
        from_attributes = True
