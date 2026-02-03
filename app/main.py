import logging
from contextlib import asynccontextmanager
from datetime import datetime
from logging.config import dictConfig

from fastapi import APIRouter, Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.core.security import validate_api_key
from app.routes.activities import router as activities_router
from app.routes.buildings import router as buildings_router
from app.routes.organizations import router as organizations_router
from app.utils.lg import logging_config

dictConfig(logging_config)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up!")
    yield
    print("Application is shutting down!")


app = FastAPI(
    lifespan=lifespan,
    dependencies=[Depends(validate_api_key)],
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "API ключ необходим для доступа ко всем эндпоинтам сервиса.",
        }
    ],
)


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


app.include_router(organizations_router)
app.include_router(buildings_router)
app.include_router(activities_router)
