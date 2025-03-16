from fastapi import APIRouter
from model.subscription import Subscription
import service.subscription as service

router = APIRouter(prefix="/subscription", tags=["creature"])

@router.get("/")
def get_all() -> list[Subscription]:
    return service.get_all()

@router.get("/{name}")
def get_one(name: str) -> Subscription:
    return service.get_one(name)

@router.post("/")
def create(subscription: Subscription) -> Subscription:
    return service.create(subscription)

@router.patch("/")
def modify(subscription: Subscription) -> Subscription:
    return service.modify(subscription)

@router.delete("/{name}")
def delete(name: str):
    return service.delete(name)