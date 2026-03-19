import logging

from fastapi import APIRouter, Query
from sqlalchemy import select

from app.db.session import async_session_factory
from app.models.database import Alert, Analysis
from app.models.schemas import AlertResponse, AnalysisResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
async def get_alerts(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Get alert history."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(Alert)
            .order_by(Alert.sent_at.desc())
            .offset(offset)
            .limit(limit)
        )
        alerts = result.scalars().all()

        response = []
        for alert in alerts:
            # Get analysis for this alert
            analysis = await session.get(Analysis, alert.analysis_id)
            analysis_resp = None
            if analysis:
                analysis_resp = AnalysisResponse(
                    id=analysis.id,
                    news_item_id=analysis.news_item_id,
                    affected_assets=analysis.affected_assets,
                    sentiment=analysis.sentiment,
                    urgency=analysis.urgency,
                    relevance_score=analysis.relevance_score,
                    confidence=analysis.confidence,
                    summary=analysis.summary,
                    created_at=analysis.created_at,
                )

            response.append(AlertResponse(
                id=alert.id,
                analysis_id=alert.analysis_id,
                sent_at=alert.sent_at,
                channel=alert.channel,
                recipient=alert.recipient,
                analysis=analysis_resp,
            ))

        return response
