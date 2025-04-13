import asyncio
import datetime

import pytz

from service.notify import send_due_reminder_email


async def scheduled_task():
    from main import supabase

    try:
        result = supabase.table("subscription_due_dates").select("due_dates").execute()
        due_dates_register = result.data[0]["due_dates"]

        utc_today_date = (
            datetime.datetime.now(pytz.utc).date().strftime("%Y-%m-%d").strip()
        )
        
        if utc_today_date not in due_dates_register:
            print(f"No subscription is due today - {utc_today_date}!")
            return

        subscriptions_due_today = due_dates_register[utc_today_date]
        for subscription in subscriptions_due_today:
            user_email = subscription["email"]
            user_name = subscription["name"]
            subscription_provider = subscription["provider"]
            subscription_type = subscription["type"]
            subscription_id = subscription["subscription_id"]
            user_id = subscription["user_id"]

            try:
                await send_due_reminder_email(
                    user_email, user_name, subscription_type, subscription_provider
                )

                print(
                    f"Reminder sent to {user_email}  on utc date {utc_today_date} as {datetime.datetime.now()}"
                )

                result = (
                    supabase.table("subscriptions")
                    .update({"ended": True})
                    .eq("id", subscription_id)
                    .eq("user_id", user_id)
                    .execute()
                )

            except Exception as e:
                print(f"Retry failed for {user_email}: {e}")

    except Exception as e:
        print(f"Failed to fetch due dates: {e}")
