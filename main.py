from database import SessionDep, create_db_and_tables
from fastapi import FastAPI, Depends
from sqlmodel import Session
from models import Post

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/posts/")
def create_post(post: Post, session: SessionDep):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post