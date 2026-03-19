import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from sqlalchemy import select, func

from app.config import get_settings
from app.db.session import async_session_factory
from app.models.database import Alert, Analysis, NewsItem, Source

logger = logging.getLogger(__name__)


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command — show system status."""
    async with async_session_factory() as session:
        sources_count = await session.execute(
            select(func.count(Source.id)).where(Source.enabled.is_(True))
        )
        news_count = await session.execute(select(func.count(NewsItem.id)))
        alerts_count = await session.execute(select(func.count(Alert.id)))

    settings = get_settings()
    text = (
        "\U0001F4CA *Nexus Status*\n\n"
        f"\U0001F7E2 System: Online\n"
        f"\U0001F4F0 Active Sources: {sources_count.scalar() or 0}\n"
        f"\U0001F4F0 Total News: {news_count.scalar() or 0}\n"
        f"\U0001F514 Total Alerts: {alerts_count.scalar() or 0}\n"
        f"\u23F1 Poll Interval: {settings.poll_interval_minutes}min\n"
        f"\U0001F916 Mode: {'Mock' if settings.mock_mode else 'Live'}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def cmd_last10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /last10 command — show last 10 alerts."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(Alert)
            .order_by(Alert.sent_at.desc())
            .limit(10)
        )
        alerts = result.scalars().all()

    if not alerts:
        await update.message.reply_text("No alerts yet.")
        return

    lines = ["\U0001F514 *Last 10 Alerts*\n"]
    for alert in alerts:
        async with async_session_factory() as session:
            analysis = await session.get(Analysis, alert.analysis_id)
            if analysis:
                news = await session.get(NewsItem, analysis.news_item_id)
                title = news.title[:50] if news else "Unknown"
                lines.append(
                    f"- [{analysis.relevance_score}/10] {title}... "
                    f"({analysis.sentiment}, {analysis.urgency})"
                )

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_pause(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pause command."""
    await update.message.reply_text("\u23F8 Nexus alerts paused. Use /resume to restart.")


async def cmd_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /resume command."""
    await update.message.reply_text("\u25B6 Nexus alerts resumed.")


def create_bot_application() -> Application:
    """Create and configure the Telegram bot application."""
    settings = get_settings()
    app = Application.builder().token(settings.telegram_bot_token).build()

    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("last10", cmd_last10))
    app.add_handler(CommandHandler("pause", cmd_pause))
    app.add_handler(CommandHandler("resume", cmd_resume))

    return app
