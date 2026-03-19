import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.config import get_settings
from app.db.init_db import init_db
from app.db.session import async_session_factory
from app.api.router import api_router
from app.models.database import Source
from app.services.scheduler_service import start_scheduler, load_schedules_on_startup, start_monitor_polling

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

# Default sources to seed
DEFAULT_SOURCES = [
    # RSS feeds
    {"name": "CoinDesk", "type": "rss", "url": "https://www.coindesk.com/arc/outboundfeeds/rss/"},
    {"name": "CoinTelegraph", "type": "rss", "url": "https://cointelegraph.com/rss"},
    {"name": "The Block", "type": "rss", "url": "https://www.theblock.co/rss.xml"},
    {"name": "Decrypt", "type": "rss", "url": "https://decrypt.co/feed"},
    # Reddit
    {"name": "r/CryptoCurrency", "type": "reddit", "url": "https://reddit.com/r/CryptoCurrency"},
    {"name": "r/Bitcoin", "type": "reddit", "url": "https://reddit.com/r/Bitcoin"},
    {"name": "r/ethfinance", "type": "reddit", "url": "https://reddit.com/r/ethfinance"},
    {"name": "r/investing", "type": "reddit", "url": "https://reddit.com/r/investing"},
    # Twitter/X
    {"name": "@CoinDesk", "type": "twitter", "url": "https://x.com/CoinDesk"},
    {"name": "@cointelegraph", "type": "twitter", "url": "https://x.com/cointelegraph"},
    {"name": "@Reuters", "type": "twitter", "url": "https://x.com/Reuters"},
    {"name": "@WSJ", "type": "twitter", "url": "https://x.com/WSJ"},
    {"name": "@federalreserve", "type": "twitter", "url": "https://x.com/federalreserve"},
]


async def _seed_sources():
    """Seed default sources if none exist."""
    async with async_session_factory() as session:
        result = await session.execute(select(Source).limit(1))
        if result.scalar_one_or_none():
            return  # Sources already exist

        for src in DEFAULT_SOURCES:
            session.add(Source(**src))
        await session.commit()
        logger.info(f"Seeded {len(DEFAULT_SOURCES)} default sources")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    if settings.mock_mode:
        logger.warning("Running in MOCK MODE — API keys not configured. Using simulated data.")
    else:
        logger.info("Running with live API keys.")

    # Initialize database tables
    await init_db()
    logger.info("Database initialized.")

    # Seed default sources
    await _seed_sources()

    # Start scheduler and restore saved schedules
    start_scheduler()
    await load_schedules_on_startup()
    logger.info("Scheduler started.")

    # Start monitor polling
    start_monitor_polling(settings.poll_interval_minutes)

    # Start Telegram bot if configured
    if settings.telegram_enabled:
        try:
            from app.alerts.bot_commands import create_bot_application
            bot_app = create_bot_application()
            await bot_app.initialize()
            await bot_app.start()
            await bot_app.updater.start_polling()
            logger.info("Telegram bot started.")
        except Exception as e:
            logger.error(f"Failed to start Telegram bot: {e}")
            bot_app = None
    else:
        bot_app = None
        logger.info("Telegram bot disabled (no token configured).")

    yield

    # Shutdown Telegram bot
    if bot_app:
        try:
            await bot_app.updater.stop()
            await bot_app.stop()
            await bot_app.shutdown()
        except Exception:
            pass


app = FastAPI(
    title="Nexus",
    description="AI-powered real-time crypto & finance surveillance system",
    version="2.0.0",
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
    settings = get_settings()
    return {
        "status": "ok",
        "service": "nexus",
        "mock_mode": settings.mock_mode,
        "telegram_enabled": settings.telegram_enabled,
        "reddit_enabled": settings.reddit_enabled,
        "twitter_enabled": settings.twitter_enabled,
    }
