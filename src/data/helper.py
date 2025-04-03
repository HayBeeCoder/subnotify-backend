
def apply_query_et_sort(query, q, sort):
    if not q and not sort:
        query.order('created_at', desc=True)
  
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
    return query


from datetime import datetime

from supabase import Client


def add_to_due_register(subscription_id: int, user_id: str, end_date: str, supabase: Client):
    deadline = end_date - 86400 # deadline is 24hrs before the end_date
    
    date_key = datetime.fromtimestamp(deadline).strftime("%Y-%m-%d")
  

    result = supabase.table("subscription_due_dates").select("due_dates").single().execute()
    due_dates = result.data["due_dates"]     

    if date_key in due_dates:
        due_dates[date_key].append({"subscription_id": subscription_id, "user_id": user_id})
    else:
        due_dates[date_key] = [{"subscription_id": subscription_id, "user_id": user_id}]    

    supabase.table("subscription_due_dates").update({"due_dates": due_dates}).eq("id", 1).execute()
    
    
    
def get_subscriptions_due_on(date: str, supabase: Client):
 
    result = supabase.table("subscription_due_dates").select("due_dates").single().execute()
    
    due_dates = result.data["due_dates"]
    return due_dates.get(date, [])  # Return list of subscriptions for that date


def get_subscriptions_register(supabase: Client):

    result = supabase.table("subscription_due_dates").select("due_dates").single().execute()
    
    due_dates = result.data["due_dates"]
    
    return due_dates # Return list of subscriptions for that date

   