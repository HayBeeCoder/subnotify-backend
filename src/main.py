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



load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

scheduler = BackgroundScheduler()

def scheduled_task():
    """This function runs at scheduled intervals."""
    print(f"Task executed at: {datetime.datetime.now()}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events."""
    print("Starting scheduler...")
    scheduler.start()
    scheduler.add_job(scheduled_task, IntervalTrigger(seconds=10), id="interval_task", replace_existing=True)
    yield
    print("Shutting down scheduler...")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
app.include_router(subscriptionrouter.router)
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
    uvicorn.run("main:app", reload=True)
    
