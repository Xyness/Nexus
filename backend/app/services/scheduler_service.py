import asyncio
import logging
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select

from app.db.session import async_session_factory
from app.models.database import Schedule, Source
from app.services.watch_service import create_report, run_watch

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def _scheduled_job(schedule_id: str, topic: str):
    """Job executed by APScheduler on cron trigger."""
    logger.info(f"Scheduled job triggered for '{topic}' (schedule={schedule_id})")
    report_id = await create_report(topic)
    await run_watch(report_id)

    # Update last_run_at
    async with async_session_factory() as session:
        schedule = await session.get(Schedule, schedule_id)
        if schedule:
            schedule.last_run_at = datetime.now(timezone.utc)
            await session.commit()


async def _poll_monitors():
    """Polling job: fetch all enabled sources and process new items."""
    from app.monitors.factory import get_monitor
    from app.services.analysis_service import process_pending_news

    logger.info("Monitor polling started")
    async with async_session_factory() as session:
        result = await session.execute(
            select(Source).where(Source.enabled.is_(True))
        )
        sources = list(result.scalars().all())

    total_new = 0
    for source in sources:
        try:
            monitor = get_monitor(source.type)
            new_items = await monitor.run(source)
            total_new += len(new_items)
        except Exception as e:
            logger.error(f"Error polling source {source.name}: {e}")

    if total_new > 0:
        logger.info(f"Polling complete: {total_new} new items from {len(sources)} sources")
        # Process pending news through analysis pipeline
        await process_pending_news()
    else:
        logger.info(f"Polling complete: no new items from {len(sources)} sources")


def _parse_cron(expression: str) -> CronTrigger:
    """Parse a cron expression (5 fields: min hour day month dow)."""
    parts = expression.strip().split()
    if len(parts) != 5:
        raise ValueError(f"Invalid cron expression: {expression}")
    return CronTrigger(
        minute=parts[0],
        hour=parts[1],
        day=parts[2],
        month=parts[3],
        day_of_week=parts[4],
    )


async def create_schedule(topic: str, cron_expression: str) -> Schedule:
    """Create a new schedule and register the APScheduler job."""
    async with async_session_factory() as session:
        schedule = Schedule(topic=topic, cron_expression=cron_expression)
        session.add(schedule)
        await session.commit()
        await session.refresh(schedule)

    trigger = _parse_cron(cron_expression)

    async def _job(sid=schedule.id, t=topic):
        await _scheduled_job(sid, t)

    scheduler.add_job(
        _job,
        trigger=trigger,
        id=schedule.id,
        replace_existing=True,
    )
    logger.info(f"Schedule created: '{topic}' with cron '{cron_expression}'")
    return schedule


async def get_schedules() -> list[Schedule]:
    """Get all schedules."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(Schedule).order_by(Schedule.created_at.desc())
        )
        return list(result.scalars().all())


async def delete_schedule(schedule_id: str) -> bool:
    """Delete a schedule and remove the APScheduler job."""
    async with async_session_factory() as session:
        schedule = await session.get(Schedule, schedule_id)
        if not schedule:
            return False
        await session.delete(schedule)
        await session.commit()

    try:
        scheduler.remove_job(schedule_id)
    except Exception:
        pass
    return True


async def load_schedules_on_startup():
    """Restore active schedules from the database."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(Schedule).where(Schedule.is_active.is_(True))
        )
        schedules = result.scalars().all()

    for s in schedules:
        try:
            trigger = _parse_cron(s.cron_expression)
            async def _job(sid=s.id, t=s.topic):
                await _scheduled_job(sid, t)

            scheduler.add_job(
                _job,
                trigger=trigger,
                id=s.id,
                replace_existing=True,
            )
            logger.info(f"Restored schedule: '{s.topic}' ({s.id})")
        except Exception as e:
            logger.error(f"Failed to restore schedule {s.id}: {e}")


def start_scheduler():
    """Start the APScheduler."""
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started")


def start_monitor_polling(interval_minutes: int = 10):
    """Add the monitor polling job to the scheduler."""
    scheduler.add_job(
        _poll_monitors,
        trigger=IntervalTrigger(minutes=interval_minutes),
        id="monitor_polling",
        replace_existing=True,
    )
    # Also run immediately on startup
    scheduler.add_job(
        _poll_monitors,
        id="monitor_polling_initial",
        replace_existing=True,
    )
    logger.info(f"Monitor polling started (every {interval_minutes} minutes)")
