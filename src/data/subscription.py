
from fastapi import HTTPException
from typing import Optional
from gotrue.types import User
from schemas.subscription import Subscription
from utils.helpers.convertToUTC import convertToUTC
from utils.helpers.calculate_durations_in_days import calculate_duration_in_days
from .helper import add_to_due_register, apply_query_et_sort, get_subscriptions_due_on, get_subscriptions_register, update_enddate


def get_all(
    user: User,
    q: Optional[str] = None,
    sort: Optional[str] = None,
):
    from main import supabase

    query = supabase.table("subscriptions").select("id,*")

    query = apply_query_et_sort(query, q, sort)
    try:

        result = query.eq("user_id", user.id) .execute()
        return {"data": result.data}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database insertion failed: {str(e)}"
        )


def create(user: User, request: Subscription):
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
        "end_date_in_utc": convertToUTC(request.end_date,request.user_timezone)
    }

    existingSubscription = (
        supabase.table("subscriptions")
        .select("*")
        .eq("provider", response_data["provider"])
        .eq("type", response_data["type"])
        .eq("user_id", response_data["user_id"])
        .execute()
    )
    if existingSubscription.data:
        raise HTTPException(
            status_code=400,
            detail="A subscription with this provider and type already exists.",
        )

    try:

        result = supabase.table("subscriptions").insert(response_data).execute()
        print(result)
        add_to_due_register(result.data[0]["id"], user, result.data[0]["end_date_in_utc"],result.data[0]["provider"], result.data[0]["type"], supabase)
        
        return {
            "message": "Subscription created successfully!",
            "subscription_id": result.data[0]["id"],  # Return the new subscription ID
            "data": result.data[0],
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database insertion failed: {str(e)}"
        )


def modify(subscription_id: int, user: User, request: Subscription):
    from main import supabase
    updated_data = {
        "provider": request.provider,
        "type": request.type,
        "description": request.description,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "user_timezone": request.user_timezone,
        "duration": calculate_duration_in_days(request.start_date, request.end_date),
        "user_id": user.id,
    }
    
    existing_subscription = supabase.table("subscriptions").select("end_date").eq("id", subscription_id).single().execute()  # Ensures only one record is returned
    
        

    try:
        result = supabase.table("subscriptions").update(updated_data).eq("id", subscription_id).eq("user_id", user.id).execute()
        # print({"result": result.data , "existing": existing_subscription.data})
        if existing_subscription.data:
            # print({"existing": existing_subscription.data["end_date"], "result": result.data[0]["end_date"]})
            if existing_subscription.data["end_date"] != result.data[0]["end_date"]:
                update_enddate(result.data[0]["end_date"],existing_subscription.data["end_date"], supabase, subscription_id)
                
        # print(get_subscriptions_register(supabase))
        return {
        "message": "Subscription updated successfully!",
        "data": result.data[0],
    }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database Update failed: {str(e)}"
        )

   

def delete(subscription_id: int, user: User):
    from main import supabase
    
    existing_subscription = (
        supabase.table("subscriptions")
        .select("id")  
        .eq("id", subscription_id)
        .eq("user_id", user.id)  
        .execute()
    )
    
    if not existing_subscription.data:
        raise HTTPException(status_code=404, detail="Subscription not found or unauthorized")
    try: 
        supabase.table("subscriptions").delete().eq("id", subscription_id).eq("user_id", user.id).execute()
    
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database Deletion failed: {str(e)}"
        )

    return {"message": "Subscription deleted successfully!"}