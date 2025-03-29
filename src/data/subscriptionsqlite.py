
'''
def create(request: DbSubscription, db: Session):
    try: 
        existing_subscription = db.query(DbSubscription).filter_by(
            provider=request.provider, type=request.type
        ).first()
        
        if existing_subscription:
            raise ValueError("Subscription with the same provider and type already exists!")

        new_subscription = DbSubscription(
            description=request.description,
            provider=request.provider,
            type=request.type,
            start_date=request.start_date,
            end_date=request.end_date,
            user_timezone=request.user_timezone,
        )
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        return new_subscription
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred: " + str(e))


def get_all(db: Session):
    return db.query(DbSubscription).all()


# def get_subscription(db: Session, service_provider_or_type: str):
#     user = db.query(DbSubscription).filter(DbSubscription.provider == service_provider_or_type).first()
#     if not user:
#         user = db.query
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Article with id {id} not found",
#         )
#     return user


# def update_user(db: Session, id: int, request: UserBase):
#     user = db.query(DbUser).filter(DbUser.id == id)
#     user.update(
#         {
#             DbUser.username: request.username,
#             DbUser.email: request.email,
#             DbUser.password: Hash.bcrypt(request.password),
#         }
#     )
#     db.commit()
#     return "ok"


# def delete_user(db: Session, id: int):
#     user = db.query(DbUser).filter(DbUser.id == id).first()
#     if user:
#         db.delete(user)
#         db.commit()
#         return "user successfully deleted!"
#     return "user not found"

'''
