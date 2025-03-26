from fastapi import APIRouter, Depends
from data.init import get_db
from schemas.subscription import Subscription
import service.subscription as service
from sqlalchemy.orm.session import Session

router = APIRouter(prefix="/subscription", tags=["subscription"])

@router.get("/")
def getAllService()-> list[Subscription]:
    return service.get_all()

@router.get("/{service_provider_or_type}")
def getService(service_provider_or_type: str) -> Subscription:
    return service.get_one(service_provider_or_type)

@router.post("/")
def create(subscription: Subscription, db: Session = Depends(get_db)) -> Subscription:
    return service.create(subscription,db)


@router.delete("/{service_id}")
def delete(id: str):
    return service.delete(id)



