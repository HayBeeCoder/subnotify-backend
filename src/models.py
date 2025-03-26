from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.sql.sqltypes import BigInteger

from data.init import Base

class DbSubscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    provider = Column(String, nullable=False)  # Provider of the subscription (e.g., Netflix)
    type = Column(String, nullable=False)  # Type of subscription (e.g., Premium)
    description = Column(String, nullable=True)  # Optional description
    start_date = Column(BigInteger, nullable=False)  # Unix timestamp for start date
    end_date = Column(BigInteger, nullable=False)  # Unix timestamp for end date
    user_timezone = Column(String, nullable=False)  # User's time zone (e.g., "America/New_York")
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to associate with a user
    __table_args__ = (UniqueConstraint('provider', 'type', name='uq_provider_type'),)