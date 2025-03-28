from pydantic import BaseModel, Field, field_validator
from typing import Optional
import pytz
from datetime import datetime
import datetime
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
     
    
    @field_validator("end_date")
    @classmethod
    def validate_start_end(cls, value: int, values):
        
        start_date = values.data.get("start_date")
        if start_date is None:
            raise ValueError("Start date must be provided before end date.")

        if value - start_date < 259200:  # 3 days in seconds
            raise ValueError("End date must be at least 3 days after the start date.")

        return value
        
    @field_validator("start_date","end_date")
    def validate_timestamp(cls, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Timestamp must be a positive integer.")

    
        dt = datetime.datetime.utcfromtimestamp(value)

        min_date = datetime.datetime(1970, 1, 1)
    

        if not (min_date <= dt):
            raise ValueError("Timestamp is out of the valid range.")
        
        return value  # Return the validated value
    
   
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
