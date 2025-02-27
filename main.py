from database import SessionDep, create_db_and_tables, get_session
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import Post, PostCreate, PostPatch
import logging

app = FastAPI()

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

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
def create_post(post: PostCreate, session: SessionDep):

    try:

        new_post = Post.model_validate(post)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)

        return new_post
    
    except Exception as e:

        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error")

@app.get("/posts/{ong_id}")
def read_posts(ong_id: int, session: Session = Depends(get_session)):

    try:

        logger.info(f"Fetching posts for ONG ID: {ong_id}")                 
        posts = session.exec(select(Post).where(Post.ong == ong_id)).all()

        if not posts:
            raise HTTPException(status_code = 404, detail = "Posts not found")
        
        return posts
    
    except Exception as e:

        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error")

@app.patch("/posts/{ong_id}/{id}")
def update_post(ong_id: int, id: int, post: PostPatch, session: Session = Depends(get_session)):

    try:

        db_post = session.get(Post, id)

        if not db_post or db_post.ong != ong_id:
            raise HTTPException(status_code = 404, detail = "Post not found")
        
        for key, value in post.model_dump(exclude_unset = True).items():
            setattr(db_post, key, value)

        session.add(db_post)
        session.commit()
        session.refresh(db_post)

        return db_post
    
    except Exception as e:

        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error")

@app.delete("/posts/{ong_id}/{id}")
def delete_post(ong_id: int, id: int, session: Session = Depends(get_session)):

    try:

        db_post = session.get(Post, id)

        if not db_post or db_post.ong != ong_id:
            raise HTTPException(status_code = 404, detail = "Post not found")
        
        session.delete(db_post)
        session.commit()

        return {"detail": "Post deleted"}
    
    except Exception as e:

        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error")