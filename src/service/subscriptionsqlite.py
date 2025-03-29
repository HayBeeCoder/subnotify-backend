from fastapi import Depends

from sqlalchemy.orm.session import Session

from schemas.subscription import CreateSubscriptionResponse, Subscription
import data.subscription as data 


def get_all(db: Session) -> list[Subscription]:
    return data.get_all(db)

def get_one(service_provider_or_type: str, db: Session) -> Subscription:
    return data.get_one(service_provider_or_type, db)

def create(subscription: Subscription, db: Session ) -> CreateSubscriptionResponse:
    return data.create( subscription, db)

def modify(subscription: Subscription, db: Session) -> Subscription:
    return data.modify(subscription, db)

def delete(service_id: str, db: Session) -> Subscription:
    return data.delete(service_id,db)