from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import Base, engine

from routes.auth import router as auth_router
from routes.pages import router as pages_router
from routes.recommendations import (
    router as recommendations_router
)


settings = get_settings()

BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered budget recommendation system",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            BASE_DIR / "static"
        )
    ),
    name="static"
)


@app.on_event("startup")
def startup():

    Base.metadata.create_all(
        bind=engine
    )


@app.get("/health")
def health():

    return {
        "status": "ok",
        "app": settings.APP_NAME
    }


app.include_router(
    pages_router
)

app.include_router(
    auth_router
)

app.include_router(
    recommendations_router
)