from typing import Optional
from fastapi import HTTPException, Header
from supabase import AuthApiError
from auth.auth import get_current_user


from db.models import DbSubscription
from utils.helpers.calculate_durations_in_days import calculate_duration_in_days


def get_all(
    authorization: str = Header(None),
    q: Optional[str] = None,
    sort: Optional[str] = None,
):
    from main import supabase

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token is required")

    user = get_current_user(supabase, authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authorization token")

    query = supabase.table("subscriptions").select("id,*")
    # .order('created_at', desc=True).execute()
    if q:
        query = query.or_(f"provider.ilike.%{q}%,type.ilike.%{q}%")

    if sort:
        if sort == "az":
            query = query.order("provider", desc=False)  # A-Z
        elif sort == "za":
            query = query.order("provider", desc=True)  # Z-A
        elif sort == "new":
            query = query.order("created_at", desc=True)  # Newest First
        elif sort == "old":
            query = query.order("created_at", desc=False)  # Oldest First
        elif sort == "short":
            query = query.order("duration", desc=False)  # Shortest Duration First
        elif sort == "long":
            query = query.order("duration", desc=True)  # Longest Duration First

    try:

        result = query.execute()
        return {"data": result.data}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database insertion failed: {str(e)}"
        )
    

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
        "duration": calculate_duration_in_days(request.start_date, request.end_date),
        "user_id": user.id,
    }

    existingSubscription = (
        supabase.table("subscriptions")
        .select("*")
        .eq("provider", response_data["provider"])
        .eq("type", response_data["type"])
        .execute()
    )
    if existingSubscription.data:
        raise HTTPException(
            status_code=400,
            detail="A subscription with this provider and type already exists.",
        )

    try:

        result = supabase.table("subscriptions").insert(response_data).execute()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database insertion failed: {str(e)}"
        )

    return {
        "message": "Subscription created successfully!",
        "subscription_id": result.data[0]["id"],  # Return the new subscription ID
        "data": result.data[0],
    }
