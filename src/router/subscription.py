from fastapi import APIRouter, Depends, Header
from data.init import get_db
from schemas.subscription import Subscription, SubscriptionsResponse
import service.subscription as service
from sqlalchemy.orm.session import Session


router = APIRouter(prefix="/subscription", tags=["subscription"])

@router.get("/")
def getAllService(db: Session = Depends(get_db)) -> list[Subscription]:
    return service.get_all(db)

@router.get("/{service_provider_or_type}")
def getService(service_provider_or_type: str, db: Session = Depends(get_db)) -> Subscription:
    return service.get_one(service_provider_or_type,db)

@router.post("/")
def create(subscription: Subscription, authorization: str = Header(None)) -> Subscription:
    return service.create(subscription,authorization)


@router.delete("/{service_id}")
def delete(service_id: str, db: Session = Depends(get_db)) -> Subscription:
    return service.delete(service_id,db)



