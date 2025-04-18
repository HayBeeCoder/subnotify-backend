from typing import Optional
from fastapi import Depends, Header
from gotrue.types import User


from schemas.subscription import (
    CreateSubscriptionResponse,
    DeleteSubscriptionResponse,
    GetAllSubscriptionsResponse,
    Subscription,
    UpdateSubscriptionResponse,
)
import data.subscription as data


def get_all(
    user: User,
    q: Optional[str] = None,
    sort: Optional[str] = None,
) -> GetAllSubscriptionsResponse:
    return data.get_all(user,q, sort)


def create(
    subscription: Subscription, user: User
) -> CreateSubscriptionResponse:
    return data.create(user, subscription)


def modify(subscription_id: int, subscription: Subscription, user: User) -> UpdateSubscriptionResponse:
    return data.modify(subscription_id, user,subscription)


def delete(subscription_id: int, user: User) -> DeleteSubscriptionResponse:
    return data.delete(subscription_id, user)
