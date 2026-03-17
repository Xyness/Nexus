from fastapi import APIRouter, HTTPException
from app.models.schemas import ReportSummary, ReportDetail
from app.services.watch_service import get_reports, get_report, delete_report

router = APIRouter()


@router.get("/reports", response_model=list[ReportSummary])
async def list_reports():
    """List all reports."""
    reports = await get_reports()
    return reports


@router.get("/reports/{report_id}", response_model=ReportDetail)
async def read_report(report_id: str):
    """Get a specific report by ID."""
    report = await get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.delete("/reports/{report_id}")
async def remove_report(report_id: str):
    """Delete a report by ID."""
    deleted = await delete_report(report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"status": "deleted"}
