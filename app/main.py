from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, notes


app = FastAPI(
    title="Day 48 - CORS and Environment Config",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
    ],
)


app.include_router(auth.router)
app.include_router(notes.router)


@app.get("/")
def root():
    return {
        "message": "Day 48 API is running",
    }


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
    }