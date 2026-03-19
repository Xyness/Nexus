import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db.session import async_session_factory
from app.models.database import Source
from app.models.schemas import SourceResponse, SourceToggleRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=list[SourceResponse])
async def get_sources():
    """Get all configured sources."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(Source).order_by(Source.type, Source.name)
        )
        return list(result.scalars().all())


@router.patch("/{source_id}", response_model=SourceResponse)
async def toggle_source(source_id: str, body: SourceToggleRequest):
    """Enable or disable a source."""
    async with async_session_factory() as session:
        source = await session.get(Source, source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        source.enabled = body.enabled
        await session.commit()
        await session.refresh(source)
        logger.info(f"Source '{source.name}' {'enabled' if body.enabled else 'disabled'}")
        return source
