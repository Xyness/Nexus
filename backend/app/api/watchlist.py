import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db.session import async_session_factory
from app.models.database import Watchlist
from app.models.schemas import WatchlistItemCreate, WatchlistItemResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.get("", response_model=list[WatchlistItemResponse])
async def get_watchlist():
    """Get all watchlist items."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(Watchlist).order_by(Watchlist.asset_symbol)
        )
        return list(result.scalars().all())


@router.post("", response_model=WatchlistItemResponse, status_code=201)
async def add_to_watchlist(item: WatchlistItemCreate):
    """Add an asset to the watchlist."""
    async with async_session_factory() as session:
        # Check for duplicate
        existing = await session.execute(
            select(Watchlist).where(Watchlist.asset_symbol == item.asset_symbol.upper())
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=409, detail=f"{item.asset_symbol} already in watchlist")

        watchlist_item = Watchlist(
            asset_symbol=item.asset_symbol.upper(),
            alert_threshold=item.alert_threshold,
        )
        session.add(watchlist_item)
        await session.commit()
        await session.refresh(watchlist_item)
        logger.info(f"Added {item.asset_symbol.upper()} to watchlist")
        return watchlist_item


@router.delete("/{item_id}")
async def remove_from_watchlist(item_id: str):
    """Remove an asset from the watchlist."""
    async with async_session_factory() as session:
        item = await session.get(Watchlist, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Watchlist item not found")
        await session.delete(item)
        await session.commit()
        logger.info(f"Removed {item.asset_symbol} from watchlist")
        return {"status": "deleted"}
