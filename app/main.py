import logging
from contextlib import asynccontextmanager
from datetime import datetime
from logging.config import dictConfig

from fastapi import APIRouter, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.utils.lg import logging_config

dictConfig(logging_config)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up!")
    yield
    print("Application is shutting down!")


app = FastAPI(lifespan=lifespan, root_path="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }
