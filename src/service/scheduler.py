from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import datetime

# Initialize the scheduler
scheduler = BackgroundScheduler()

def send_reminder_email():
    """Simulates sending a reminder email (Replace with actual email logic)"""
    print(f"📧 Reminder email sent at: {datetime.datetime.now()}")

# Predefined Short Intervals for Quick Testing
scheduler.add_job(send_reminder_email, IntervalTrigger(seconds=10), id="every_10_sec", replace_existing=True)  # Every 10 sec
scheduler.add_job(send_reminder_email, IntervalTrigger(minutes=1), id="every_minute", replace_existing=True)  # Every 1 min
