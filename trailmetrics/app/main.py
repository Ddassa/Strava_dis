import os
from fastapi import FastAPI
from dotenv import load_dotenv

from . import auth, webhook, db

load_dotenv()

app = FastAPI(title="Trailmetrics")
app.include_router(auth.router)
app.include_router(webhook.router)

@app.on_event("startup")
async def startup_event():
    db.init_db()

