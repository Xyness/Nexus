import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.init_db import init_db
from app.api.router import api_router
from app.services.scheduler_service import start_scheduler, load_schedules_on_startup

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    if settings.mock_mode:
        logger.warning("⚠ Running in MOCK MODE — API keys not configured. Using simulated data.")
    else:
        logger.info("Running with live API keys.")

    # Initialize database tables
    await init_db()
    logger.info("Database initialized.")

    # Start scheduler and restore saved schedules
    start_scheduler()
    await load_schedules_on_startup()
    logger.info("Scheduler started.")

    yield


app = FastAPI(
    title="AlphaWatch",
    description="AI-powered financial market intelligence agent",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok", "mock_mode": get_settings().mock_mode}
