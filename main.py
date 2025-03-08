from database import create_db_and_tables
from fastapi import FastAPI
import logging
from routes import posts, profiles

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(profiles.router, prefix="/profiles", tags=["profiles"])