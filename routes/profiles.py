from database import SessionDep, get_session
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Profile, ProfileCreate
import logging
import time

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/")
def create_profile(profile: Profile, session: SessionDep):
    try:
        logger.info("Request initiated: POST /profile/")
        start_time = time.perf_counter()

        new_profile = profile
        session.add(new_profile)
        session.commit()
        session.refresh(new_profile)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info("Request finalized successfully: POST /profile/")
        logger.info(f"Execution time: {elapsed_time:.6f} seconds")

        return new_profile

    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{ong_id}")
def read_profiles(ong_id: int, session: Session = Depends(get_session)):
    try:
        logger.info(f"Request initiated: GET /profile/{ong_id}")
        start_time = time.perf_counter()

        logger.info(f"Fetching profile for ONG ID: {ong_id}")
        profile = session.exec(select(Profile).where(Profile.ong == ong_id)).first()

        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info(f"Request finalized successfully: GET /profile/{ong_id}")
        logger.info(f"Execution time: {elapsed_time:.6f} seconds")

        return profile

    except Exception as e:
        logger.error(f"Error fetching profile: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{ong_id}/{id}")
def delete_profile(ong_id: int, id: int, session: Session = Depends(get_session)):
    try:
        logger.info(f"Request initiated: DELETE /profile/{ong_id}/{id}")
        start_time = time.perf_counter()

        db_profile = session.get(Profile, id)

        if not db_profile or db_profile.ong != ong_id:
            raise HTTPException(status_code=404, detail="Profile not found")

        session.delete(db_profile)
        session.commit()

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info(f"Request finalized successfully: DELETE /profile/{ong_id}/{id}")
        logger.info(f"Execution time: {elapsed_time:.6f} seconds")

        return {"detail": "Profile deleted"}

    except Exception as e:
        logger.error(f"Error deleting profile: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")