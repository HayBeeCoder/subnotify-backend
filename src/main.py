import datetime
import os

from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from router import subscription as subscriptionrouter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from supabase import create_client, Client 

   
from slowapi import Limiter, _rate_limit_exceeded_handler

from slowapi.errors import RateLimitExceeded

from utils.helpers.limiting_config import limiter


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

scheduler = BackgroundScheduler()

def scheduled_task():
    result = supabase.table("subscription_due_dates").select("due_dates").execute()
    due_dates_register = result.data[0]['due_dates']
    """This function runs at scheduled intervals."""
    print(f"Task executed at: {datetime.datetime.now()}")
    print({"data": due_dates_register})

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events."""
    print("Starting scheduler...")
    scheduler.start()
    scheduler.add_job(scheduled_task, IntervalTrigger(seconds=30), id="interval_task", replace_existing=True)
    yield
    print("Shutting down scheduler...")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
app.include_router(subscriptionrouter.router)
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Fallback to 8000 locally
    print(port)
    uvicorn.run("main:app", host="0.0.0.0", port=port)
    
