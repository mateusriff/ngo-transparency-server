from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from fastapi import FastAPI
import logging
from routes import posts, profiles

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Permitir apenas o front-end local
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(profiles.router, prefix="/profiles", tags=["profiles"])