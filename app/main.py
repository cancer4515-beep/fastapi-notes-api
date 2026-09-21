from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, notes


openapi_tags = [
    {
        "name": "System",
        "description": "Kiểm tra trạng thái API.",
    },
    {
        "name": "Auth",
        "description": (
            "Đăng ký, đăng nhập và "
            "thông tin người dùng hiện tại."
        ),
    },
    {
        "name": "Notes",
        "description": (
            "CRUD notes của người dùng. "
            "Yêu cầu JWT authentication."
        ),
    },
]


app = FastAPI(
    title="FastAPI Notes API",
    version="1.1.0",
    openapi_tags=openapi_tags,
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


@app.get("/", tags=["System"])
def root():
    return {
        "message": "FastAPI Notes API is running",
    }


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
    }