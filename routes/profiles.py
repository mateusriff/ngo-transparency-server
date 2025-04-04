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
        logger.info("Request initiated: POST /profiles/")
        start_time = time.perf_counter()

        new_profile = profile
        session.add(new_profile)
        session.commit()
        session.refresh(new_profile)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info("Request finalized successfully: POST /profiles/")
        logger.info(f"Execution time: {elapsed_time:.6f} seconds")

        return new_profile

    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{ong_id}")
def read_profiles(ong_id: int, session: Session = Depends(get_session)):
    try:
        logger.info(f"Request initiated: GET /profiles/{ong_id}")
        start_time = time.perf_counter()

        logger.info(f"Fetching profiles for ONG ID: {ong_id}")
        profiles = session.exec(select(Profile).where(Profile.ong == ong_id)).all()

        if not profiles:
            raise HTTPException(status_code=404, detail="Profiles not found")

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info(f"Request finalized successfully: GET /profiles/{ong_id}")
        logger.info(f"Execution time: {elapsed_time:.6f} seconds")

        return profiles

    except Exception as e:
        logger.error(f"Error fetching profiles: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{ong_id}/{id}")
def delete_profile(ong_id: int, id: int, session: Session = Depends(get_session)):
    try:
        logger.info(f"Request initiated: DELETE /profiles/{ong_id}/{id}")
        start_time = time.perf_counter()

        db_profile = session.get(Profile, id)

        if not db_profile or db_profile.ong != ong_id:
            raise HTTPException(status_code=404, detail="Profile not found")

        session.delete(db_profile)
        session.commit()

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info(f"Request finalized successfully: DELETE /profiles/{ong_id}/{id}")
        logger.info(f"Execution time: {elapsed_time:.6f} seconds")

        return {"detail": "Profile deleted"}

    except Exception as e:
        logger.error(f"Error deleting profile: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")