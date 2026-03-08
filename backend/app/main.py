import sentry_sdk
import os
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=1.0,  # Ajustez en production (ex: 0.1)
)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="WAHID Platform API",
    description="API principale de la plateforme WAHID - Module Transport",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🚀 WAHID Platform API - Bienvenue!",
        "version": "1.0.0",
        "module": "Transport",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "WAHID Backend"}

@app.get("/api/v1/info")
async def api_info():
    return {
        "name": "WAHID Platform",
        "version": "1.0.0",
        "modules": ["Transport", "CRM", "Marketplace"],
        "phase": "Development"
    }

from app.api import auth

app.include_router(auth.router)

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gère le cycle de vie"""
    # ===== STARTUP =====
    logger.info("🚀 Starting WAHID Platform")
    
    # Créer tables automatiquement
    from app.core.database import create_tables
    await create_tables()
    logger.info("✅ Database ready")
    
    yield
    
    # ===== SHUTDOWN =====
    from app.core.database import engine
    await engine.dispose()
    logger.info("👋 Shutdown complete")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
