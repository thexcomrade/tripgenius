from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.database.db import create_database

from app.api.auth import router as auth_router

from app.api.trip import router as trip_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()

    print()
    print("=" * 60)
    print(f"{settings.APP_NAME} Backend Started")
    print("=" * 60)
    print()

    yield

    print()
    print("=" * 60)
    print(f"{settings.APP_NAME} Backend Stopped")
    print("=" * 60)
    print()


app = FastAPI(
    title=settings.APP_NAME,
    description=("AI Powered Sustainable Travel Planning Platform"),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)

app.include_router(trip_router)

from pydantic import BaseModel
from app.services.ai_service import get_ai_service


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
async def chat_with_ai(request: ChatRequest) -> dict:
    ai_service = get_ai_service()
    result = ai_service.generate_chat_response(request.message)
    return result


@app.get("/")
async def root() -> dict:

    return {
        "application": settings.APP_NAME,
        "status": "running",
        "version": "1.0.0",
        "environment": settings.APP_ENV,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/version")
async def version() -> dict:

    return {
        "application": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.APP_ENV,
    }


@app.get("/status")
async def status() -> dict:

    return {
        "healthy": True,
        "database": True,
        "authentication": True,
        "trip_service": True,
        "ai_service": True,
        "weather_service": True,
        "recommendation_service": True,
    }
