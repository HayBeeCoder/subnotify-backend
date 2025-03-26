# from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from models.subscription import DbSubscription
from schemas import subscription
# from schemas import UserBase


def create(db: Session, request: DbSubscription):
    
    new_subscription = subscription(
        description=request.description,
        provider=request.provider,
        type=request.type,
        start_date= request.start_date,
        end_date=request.end_date,
        user_timezone=request.user_timezone
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription
    """
 

def get_all_users(db: Session):
    return db.query(DbUser).all()


def get_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id {id} not found",
        )
    return user


def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    user.update(
        {
            DbUser.username: request.username,
            DbUser.email: request.email,
            DbUser.password: Hash.bcrypt(request.password),
        }
    )
    db.commit()
    return "ok"


def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if user:
        db.delete(user)
        db.commit()
        return "user successfully deleted!"
    return "user not found"
   
    
    """