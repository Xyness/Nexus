from fastapi import APIRouter, HTTPException
from app.models.schemas import ScheduleCreateRequest, ScheduleResponse
from app.services.scheduler_service import create_schedule, get_schedules, delete_schedule

router = APIRouter()


@router.post("/schedule", response_model=ScheduleResponse)
async def add_schedule(req: ScheduleCreateRequest):
    """Create a new scheduled watch."""
    schedule = await create_schedule(req.topic, req.cron_expression)
    return schedule


@router.get("/schedule", response_model=list[ScheduleResponse])
async def list_schedules():
    """List all schedules."""
    return await get_schedules()


@router.delete("/schedule/{schedule_id}")
async def remove_schedule(schedule_id: str):
    """Delete a schedule."""
    deleted = await delete_schedule(schedule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"status": "deleted"}
