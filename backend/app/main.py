from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def create_app() -> FastAPI:
    app = FastAPI(
        title="MSN Automacao API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    @app.get("/api/v1/health", tags=["health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
