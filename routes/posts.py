from database import SessionDep, get_session
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Post, PostCreate, PostPatch
import logging
import time

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/")
def create_post(post: PostCreate, session: SessionDep):
    try:
        logger.info("Request initiated: POST /posts/")
        start_time = time.perf_counter()

        new_post = Post.model_validate(post)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info("Request finalized successfully: POST /posts/")
        logger.info(f"Execution time: {elapsed_time:.6f} seconds")

        return new_post

    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{ong_id}")
def read_posts(ong_id: int, session: Session = Depends(get_session)):
    try:
        logger.info(f"Request initiated: GET /posts/{ong_id}")
        start_time = time.perf_counter()

        logger.info(f"Fetching posts for ONG ID: {ong_id}")
        posts = session.exec(select(Post).where(Post.ong == ong_id)).all()

        if not posts:
            raise HTTPException(status_code=404, detail="Posts not found")

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info(f"Request finalized successfully: GET /posts/{ong_id}")
        logger.info(f"Execution time: {elapsed_time:.6f} seconds")

        return posts

    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/{ong_id}/{id}")
def update_post(ong_id: int, id: int, post: PostPatch, session: Session = Depends(get_session)):
    try:
        logger.info(f"Request initiated: PATCH /posts/{ong_id}/{id}")
        start_time = time.perf_counter()

        db_post = session.get(Post, id)

        if not db_post or db_post.ong != ong_id:
            raise HTTPException(status_code=404, detail="Post not found")

        for key, value in post.model_dump(exclude_unset=True).items():
            setattr(db_post, key, value)

        session.add(db_post)
        session.commit()
        session.refresh(db_post)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info(f"Request finalized successfully: PATCH /posts/{ong_id}/{id}")
        logger.info(f"Execution time: {elapsed_time:.6f} seconds")

        return db_post

    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{ong_id}/{id}")
def delete_post(ong_id: int, id: int, session: Session = Depends(get_session)):
    try:
        logger.info(f"Request initiated: DELETE /posts/{ong_id}/{id}")
        start_time = time.perf_counter()

        db_post = session.get(Post, id)

        if not db_post or db_post.ong != ong_id:
            raise HTTPException(status_code=404, detail="Post not found")

        session.delete(db_post)
        session.commit()

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info(f"Request finalized successfully: DELETE /posts/{ong_id}/{id}")
        logger.info(f"Execution time: {elapsed_time:.6f} seconds")

        return {"detail": "Post deleted"}

    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")