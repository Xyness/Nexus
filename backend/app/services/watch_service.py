import asyncio
import logging
from datetime import datetime, timezone

from sqlalchemy import select
from app.db.session import async_session_factory
from app.agent.graph import agent
from app.models.database import Report

logger = logging.getLogger(__name__)


async def create_report(topic: str) -> str:
    """Create a pending report and return its ID."""
    async with async_session_factory() as session:
        report = Report(topic=topic, status="pending")
        session.add(report)
        await session.commit()
        await session.refresh(report)
        return report.id


async def run_watch(report_id: str):
    """Execute the agent pipeline and persist results."""
    # Mark as running
    async with async_session_factory() as session:
        report = await session.get(Report, report_id)
        if not report:
            logger.error(f"Report {report_id} not found")
            return
        report.status = "running"
        await session.commit()

    try:
        # Run the synchronous LangGraph agent in a thread
        result = await asyncio.to_thread(
            agent.invoke,
            {
                "topic": report.topic,
                "sub_questions": [],
                "search_results": [],
                "summaries": [],
                "sentiment": "neutral",
                "sentiment_score": 0.5,
                "key_facts": [],
                "report_md": "",
                "errors": [],
            },
        )

        # Persist results
        async with async_session_factory() as session:
            report = await session.get(Report, report_id)
            report.status = "completed"
            report.content_md = result.get("report_md", "")
            report.sentiment = result.get("sentiment", "neutral")
            report.sentiment_score = result.get("sentiment_score", 0.5)
            search_results = result.get("search_results", [])
            report.sources_count = len(search_results)
            # Deduplicate sources by URL and store title+url
            seen_urls = set()
            sources = []
            for sr in search_results:
                url = sr.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    sources.append({"title": sr.get("title", ""), "url": url})
            report.sources = sources
            report.sub_questions = result.get("sub_questions", [])
            report.completed_at = datetime.now(timezone.utc)
            if result.get("errors"):
                report.error_message = "; ".join(result["errors"])
            await session.commit()

        logger.info(f"Report {report_id} completed successfully")

    except Exception as e:
        logger.exception(f"Report {report_id} failed")
        async with async_session_factory() as session:
            report = await session.get(Report, report_id)
            report.status = "error"
            report.error_message = str(e)
            report.completed_at = datetime.now(timezone.utc)
            await session.commit()


async def get_reports() -> list[Report]:
    """Get all reports ordered by creation date."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(Report).order_by(Report.created_at.desc())
        )
        return list(result.scalars().all())


async def get_report(report_id: str) -> Report | None:
    """Get a single report by ID."""
    async with async_session_factory() as session:
        return await session.get(Report, report_id)


async def delete_report(report_id: str) -> bool:
    """Delete a report by ID. Returns True if deleted."""
    async with async_session_factory() as session:
        report = await session.get(Report, report_id)
        if not report:
            return False
        await session.delete(report)
        await session.commit()
        return True
