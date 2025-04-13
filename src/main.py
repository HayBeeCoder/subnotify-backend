
import os

from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from router import subscription as subscriptionrouter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from supabase import create_client, Client 

   
from slowapi import  _rate_limit_exceeded_handler

from slowapi.errors import RateLimitExceeded

from service.scheduler import scheduled_task
from utils.helpers.limiting_config import limiter


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events."""
    print("Starting scheduler...")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_task, "cron", hour=0, minute=0)
    scheduler.start()
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
    
