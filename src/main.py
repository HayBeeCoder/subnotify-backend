from fastapi import FastAPI
from db import models
from router import subscription as subscriptionrouter
from data.init import engine

app = FastAPI()
app.include_router(subscriptionrouter.router)


models.Base.metadata.create_all(bind=engine)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
    
