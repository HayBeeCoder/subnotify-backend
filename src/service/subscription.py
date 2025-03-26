from fastapi import Depends

from sqlalchemy.orm.session import Session

from schemas.subscription import Subscription
import data.subscription as data 
from data.init import get_db

# def get_all() -> list[Subscription]:
#     return data.get_all()

# def get_one(name: str) -> Subscription:
#     return data.get_one(name)

def create(subscription: Subscription, db: Session ) -> Subscription:

    return data.create( subscription, db)

# def modify(subscription: Subscription) -> Subscription:
#     return data.modify(subscription)

# def delete(name: str) -> bool:
#     return data.delete(name)