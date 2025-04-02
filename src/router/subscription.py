from typing import Optional
from fastapi import APIRouter, Depends, Header,Query
from data.init import get_db
from user import get_current_user
from schemas.subscription import (
    CreateSubscriptionResponse,
    GetAllSubscriptionsResponse,
    Subscription,
    SubscriptionsResponse,
)
import service.subscription as service
from sqlalchemy.orm.session import Session


router = APIRouter(prefix="/subscription", tags=["subscription"], dependencies=[Depends(get_current_user)])


# @router.get("/subscriptions")
@router.get("/all")
@router.get("/all/")
def get_all(
    authorization: str = Header(None),
    q: Optional[str] = Query(
        None, description="Search query for filtering subscriptions"
    ),
    sort: Optional[str] = Query(
        None, description="Sort order: az, za, new, old, long, short"
    ),
) -> GetAllSubscriptionsResponse:
    return service.get_all(authorization,q, sort)


@router.get("/{service_provider_or_type}")
def getService(
    service_provider_or_type: str, db: Session = Depends(get_db)
) -> Subscription:
    return service.get_one(service_provider_or_type, db)


@router.post("/")
def create(
    subscription: Subscription, authorization: str = Header(None)
) -> CreateSubscriptionResponse:
    return service.create(subscription, authorization)


@router.delete("/{service_id}")
def delete(service_id: str, db: Session = Depends(get_db)) -> Subscription:
    return service.delete(service_id, db)
