def apply_query_et_sort(query, q, sort):
    if not q and not sort:
        query.order("created_at", desc=True)

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

from gotrue.types import User


def add_to_due_register(
    subscription_id: int, user: User, end_date: str,provider: str, type: str, supabase: Client
):
    user_id = user.id
    deadline = end_date - 86400  # deadline is 24hrs before the end_date

    date_key = datetime.fromtimestamp(deadline).strftime("%Y-%m-%d")

    result = (
        supabase.table("subscription_due_dates").select("due_dates").single().execute()
    )
    due_dates = result.data["due_dates"]

    if date_key in due_dates:
        due_dates[date_key].append(
            {
                "subscription_id": subscription_id,
                "user_id": user_id,
                "email": user.user_metadata["email"],
                "name": user.user_metadata["full_name"],
                "provider": provider,
                "type": type
            }
        )
    else:
        due_dates[date_key] = [
            {
                "subscription_id": subscription_id,
                "user_id": user_id,
                "email": user.user_metadata["email"],
                "name": user.user_metadata["full_name"],
                "provider": provider,
                "type": type
            }
        ]

    supabase.table("subscription_due_dates").update({"due_dates": due_dates}).eq(
        "id", 1
    ).execute()


def get_subscriptions_due_on(end_date: int, supabase: Client):
    deadline = end_date - 86400  # deadline is 24hrs before the end_date

    date_key = datetime.fromtimestamp(deadline).strftime("%Y-%m-%d")

    result = (
        supabase.table("subscription_due_dates").select("due_dates").single().execute()
    )

    due_dates = result.data["due_dates"]
    return due_dates.get(date_key, [])  # Return list of subscriptions for that date


def get_subscriptions_register(supabase: Client):

    result = (
        supabase.table("subscription_due_dates").select("due_dates").single().execute()
    )

    due_dates = result.data["due_dates"]

    return due_dates  # Return list of subscriptions for that date


def update_enddate(
    new_enddate: int, old_enddate: int, supabase: Client, subscription_id: int
):
    old_deadline = old_enddate - 86400  # deadline is 24hrs before the end_date
    new_deadline = new_enddate - 86400

    old_date_key = datetime.fromtimestamp(old_deadline).strftime("%Y-%m-%d")
    new_date_key = datetime.fromtimestamp(new_deadline).strftime("%Y-%m-%d")

    result = (
        supabase.table("subscription_due_dates")
        .select("id, due_dates")
        .single()
        .execute()
    )
    # due_dates = result.data["due_dates"]

    due_dates = result.data.get("due_dates", {})  # Ensure it's a dictionary
    # Remove subscription from the old date key
    subscription_entry = None
    if old_date_key in due_dates:
        for i, obj in enumerate(due_dates[old_date_key]):
            if obj["subscription_id"] == subscription_id:
                subscription_entry = due_dates[old_date_key].pop(i)
                break

        # If the list becomes empty, delete the key
    if not bool(len(due_dates[old_date_key])):
        del due_dates[old_date_key]

    if subscription_entry:
        if new_date_key not in due_dates:
            due_dates[new_date_key] = []

        due_dates[new_date_key].append(subscription_entry)

        # Update the record in the database

    update_result = (
        supabase.table("subscription_due_dates")
        .update({"due_dates": due_dates})
        .eq("id", result.data["id"])
        .execute()
    )
    # print({"message": "End date updated successfully", "due_dates": due_dates})
