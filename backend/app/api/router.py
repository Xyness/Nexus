from fastapi import APIRouter
from app.api.watch import router as watch_router
from app.api.reports import router as reports_router
from app.api.schedule import router as schedule_router
from app.api.news import router as news_router
from app.api.alerts import router as alerts_router
from app.api.watchlist import router as watchlist_router
from app.api.sources import router as sources_router

api_router = APIRouter()
api_router.include_router(watch_router, tags=["watch"])
api_router.include_router(reports_router, tags=["reports"])
api_router.include_router(schedule_router, tags=["schedule"])
api_router.include_router(news_router, tags=["news"])
api_router.include_router(alerts_router, tags=["alerts"])
api_router.include_router(watchlist_router, tags=["watchlist"])
api_router.include_router(sources_router, tags=["sources"])
