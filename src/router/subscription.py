from typing import Optional
from fastapi import APIRouter, Depends, Header, Query, Request
from slowapi import Limiter
from auth.auth import get_authenticated_user

from user import get_current_user
from schemas.subscription import (
    CreateSubscriptionResponse,
    DeleteSubscriptionResponse,
    GetAllSubscriptionsResponse,
    Subscription,
    UpdateSubscriptionResponse,
)
import service.subscription as service
from utils.helpers.limiting_config import limiter


router = APIRouter(
    prefix="/subscription",
    tags=["subscription"],
    dependencies=[Depends(get_current_user)],
)



@router.get("/all")
@limiter.limit("5/minute")
def get_all(
    request: Request,
    user: dict = Depends(get_authenticated_user),
    q: Optional[str] = Query(
        None, description="Search query for filtering subscriptions"
    ),
    sort: Optional[str] = Query(
        None, description="Sort order: az, za, new, old, long, short"
    ),
) -> GetAllSubscriptionsResponse:
    return service.get_all(user, q, sort)



@router.post("/")
@limiter.limit("5/minute")
def create(
    request: Request,
    subscription: Subscription, user: dict = Depends(get_authenticated_user)
) -> CreateSubscriptionResponse:
    return service.create(subscription, user)


@router.put("/{subscription_id}")
@limiter.limit("5/minute")
def modify(
    request: Request,
    subscription_id: int,
    subscription: Subscription,
    user: dict = Depends(get_authenticated_user),
) -> UpdateSubscriptionResponse:
    return service.modify(subscription_id, subscription, user)

#   "end_date": 1714502400,

@router.delete("/{subscription_id}")
@limiter.limit("5/minute")
def delete(request: Request, subscription_id: int, user: dict = Depends(get_authenticated_user)) -> DeleteSubscriptionResponse :
    return service.delete(subscription_id, user)
