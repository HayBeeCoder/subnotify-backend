from fastapi import HTTPException
from typing import Optional
from gotrue.types import User
from db.models import DbSubscription
from utils.helpers.calculate_durations_in_days import calculate_duration_in_days
from .helper import apply_query_et_sort


def get_all(
    user: User,
    q: Optional[str] = None,
    sort: Optional[str] = None,
):
    from main import supabase

    query = supabase.table("subscriptions").select("id,*")
    # .order('created_at', desc=True).execute()
    query = apply_query_et_sort(query, q, sort)
    try:

        result = query.execute()
        return {"data": result.data}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database insertion failed: {str(e)}"
        )


def create(user: User, request: DbSubscription):
    from main import supabase

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
