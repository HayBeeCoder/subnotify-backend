from typing import Optional
from fastapi import Depends, Header

from sqlalchemy.orm.session import Session

from schemas.subscription import (
    CreateSubscriptionResponse,
    GetAllSubscriptionsResponse,
    Subscription,
)
import data.subscription as data


def get_all(
    authorization: str = Header(None),
    q: Optional[str] = None,
    sort: Optional[str] = None,
) -> GetAllSubscriptionsResponse:
    return data.get_all(authorization,q, sort)


def get_one(service_provider_or_type: str, db: Session) -> Subscription:
    return data.get_one(service_provider_or_type, db)


def create(
    subscription: Subscription, authorization: str = Header(None)
) -> CreateSubscriptionResponse:
    return data.create(subscription, authorization)


def modify(subscription: Subscription, db: Session) -> Subscription:
    return data.modify(subscription, db)


def delete(service_id: str, db: Session) -> Subscription:
    return data.delete(service_id, db)
