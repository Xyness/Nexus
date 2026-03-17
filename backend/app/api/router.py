from fastapi import APIRouter
from app.api.watch import router as watch_router
from app.api.reports import router as reports_router
from app.api.schedule import router as schedule_router

api_router = APIRouter()
api_router.include_router(watch_router, tags=["watch"])
api_router.include_router(reports_router, tags=["reports"])
api_router.include_router(schedule_router, tags=["schedule"])
