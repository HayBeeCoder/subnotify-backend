from fastapi import APIRouter, Depends
from data.init import get_db
from schemas.subscription import Subscription
import service.subscription as service
from sqlalchemy.orm.session import Session

router = APIRouter(prefix="/subscription", tags=["subscription"])

# @router.get("/")
# def get_all() -> list[Subscription]:
#     return service.get_all()


# @router.get("/{name}")
# def get_one(name: str) -> Subscription:
#     return service.get_one(name)

@router.post("/")
def create(subscription: Subscription, db: Session = Depends(get_db)) -> Subscription:
    return service.create(subscription,db)


# @router.patch("/")
# def modify(subscription: Subscription) -> Subscription:
#     return service.modify(subscription)

# @router.delete("/{name}")
# def delete(name: str):
#     return service.delete(name)


