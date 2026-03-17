from fastapi import APIRouter, BackgroundTasks
from app.models.schemas import WatchRequest, WatchResponse
from app.services.watch_service import create_report, run_watch

router = APIRouter()


@router.post("/watch", response_model=WatchResponse)
async def trigger_watch(req: WatchRequest, background_tasks: BackgroundTasks):
    """Trigger a new market watch analysis."""
    report_id = await create_report(req.topic)
    background_tasks.add_task(run_watch, report_id)
    return WatchResponse(report_id=report_id, status="pending")
