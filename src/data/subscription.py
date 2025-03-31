from fastapi import HTTPException, Header
from sqlalchemy.orm.session import Session
from auth.auth import get_current_user


from db.models import DbSubscription

def create(request: DbSubscription, authorization: str = Header(None)):
   

    from main import supabase
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token is required")
    

    user = get_current_user(supabase, authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authorization token")
   
    response_data = {
        "provider": request.provider,
        "type": request.type,
        "description": request.description,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "user_timezone": request.user_timezone,
        "user_id": user.id  
    }
    
    existingSubscription = supabase.table("subscriptions").select("*").eq("provider", response_data["provider"]).eq("type", response_data["type"]).execute()
    if existingSubscription.data:
        raise HTTPException(status_code=400, detail="A subscription with this provider and type already exists.")

    
    try:
        
        result = supabase.table("subscriptions").insert(response_data).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database insertion failed: {str(e)}")

    
    

    return {
        "message": "Subscription created successfully!",
        "subscription_id": result.data[0]["id"],  # Return the new subscription ID
        "data": result.data[0]
    }
