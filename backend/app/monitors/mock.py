import random
import time
import logging

from app.models.database import Source
from app.monitors.base import BaseMonitor

logger = logging.getLogger(__name__)

# Realistic mock news templates
_CRYPTO_NEWS = [
    ("Bitcoin Breaks Past ${price}K as Institutional Demand Surges", "Bitcoin rallied past ${price},000 today as institutional investors continue accumulating. ETF inflows reached ${flow}M this week."),
    ("Ethereum Foundation Announces Major Protocol Upgrade", "The Ethereum Foundation revealed plans for a significant protocol upgrade targeting improved scalability and reduced gas fees."),
    ("SEC Chair Signals More Crypto-Friendly Regulatory Framework", "In a recent speech, the SEC chair indicated a shift toward more accommodating crypto regulations, boosting market sentiment."),
    ("Solana DeFi TVL Hits All-Time High of ${tvl}B", "Solana's DeFi ecosystem reached a record ${tvl} billion in Total Value Locked, driven by new lending protocols."),
    ("Major Bank Launches Crypto Custody Service for Institutional Clients", "A top-5 global bank announced its entry into crypto custody, signaling mainstream financial adoption."),
    ("Stablecoin Market Cap Crosses $200B Milestone", "The combined market cap of stablecoins surpassed $200 billion, reflecting growing demand for crypto dollar assets."),
    ("Layer 2 Solutions See Record Transaction Volume", "Ethereum L2 networks processed a combined record of ${txns}M transactions this week, up 45% from last month."),
    ("Crypto Exchange Reports Record Q1 Trading Volume", "A leading crypto exchange reported $${vol}B in Q1 trading volume, its highest quarterly figure ever."),
    ("Central Bank Digital Currency Pilot Expands to 5 New Countries", "The BIS-backed CBDC pilot program expanded its reach, adding five new participating nations this quarter."),
    ("DeFi Protocol Suffers ${loss}M Exploit Through Flash Loan Attack", "A popular DeFi lending protocol was exploited for ${loss} million through a sophisticated flash loan attack."),
]

_FINANCE_NEWS = [
    ("Fed Holds Rates Steady, Signals Potential Cut in Q3", "The Federal Reserve kept interest rates unchanged but hinted at a possible rate cut later this year amid cooling inflation."),
    ("S&P 500 Hits New All-Time High on Tech Earnings Beat", "The S&P 500 index reached a fresh record high, driven by better-than-expected earnings from major tech companies."),
    ("Oil Prices Surge ${pct}% on OPEC+ Supply Cut Extension", "Crude oil prices jumped ${pct}% after OPEC+ members agreed to extend production cuts through the end of the year."),
    ("Global Bond Yields Drop as Recession Fears Resurface", "Government bond yields declined across major economies as investors sought safe havens amid renewed recession concerns."),
    ("Major Tech Company Announces $${bb}B Stock Buyback Program", "A leading technology company unveiled a massive ${bb} billion share repurchase program, boosting investor confidence."),
    ("Unemployment Claims Fall to 6-Month Low", "Weekly jobless claims dropped to their lowest level in six months, suggesting continued labor market strength."),
    ("Gold Rallies to ${gold} as Dollar Weakens", "Gold prices surged to ${gold} per ounce as the US dollar index fell to a multi-month low."),
    ("European Markets Close Higher on Strong PMI Data", "European stock markets rallied after purchasing managers' index data exceeded expectations across the eurozone."),
]

_REDDIT_TITLES = [
    "[Discussion] Is {asset} about to break out? Technical analysis inside",
    "Unpopular opinion: {asset} is undervalued at current levels",
    "{asset} whale just moved ${amount}M — what does this mean?",
    "Just read the {asset} whitepaper update. Here's what's changing.",
    "Why I'm accumulating {asset} at these levels — DD inside",
    "Breaking: Major partnership announcement for {asset}",
    "{asset} network metrics are at all-time highs. Charts inside.",
    "Warning: {asset} showing bearish divergence on the 4H chart",
]

_TWITTER_POSTS = [
    "Breaking: {asset} just hit ${price}. Market sentiment shifting rapidly.",
    "Just published our Q2 outlook for {asset}. Key levels to watch: {support} support, {resistance} resistance.",
    "Institutional flows into {asset} products reached ${flow}M this week. Trend acceleration.",
    "Regulatory update: new framework for {asset} trading expected by Q3.",
    "On-chain data shows smart money accumulating {asset} aggressively this week.",
]


class MockRSSMonitor(BaseMonitor):
    """Mock RSS monitor that generates realistic crypto/finance news."""

    async def fetch(self, source: Source) -> list[dict]:
        rng = random.Random(time.time())

        # Generate 1-3 news items per fetch
        count = rng.randint(1, 3)
        pool = _CRYPTO_NEWS if "crypto" in source.name.lower() or "coin" in source.name.lower() else _FINANCE_NEWS
        items = []

        for _ in range(count):
            template_title, template_content = rng.choice(pool)
            # Fill in random values
            title = template_title.replace("${price}", str(rng.randint(60, 120)))
            title = title.replace("${flow}", str(rng.randint(100, 800)))
            title = title.replace("${tvl}", f"{rng.uniform(5, 30):.1f}")
            title = title.replace("${txns}", str(rng.randint(10, 50)))
            title = title.replace("${vol}", str(rng.randint(500, 2000)))
            title = title.replace("${loss}", str(rng.randint(5, 100)))
            title = title.replace("${pct}", f"{rng.uniform(2, 8):.1f}")
            title = title.replace("${bb}", str(rng.randint(5, 50)))
            title = title.replace("${gold}", str(rng.randint(2200, 2800)))

            content = template_content.replace("${price}", str(rng.randint(60, 120)))
            content = content.replace("${flow}", str(rng.randint(100, 800)))
            content = content.replace("${tvl}", f"{rng.uniform(5, 30):.1f}")
            content = content.replace("${txns}", str(rng.randint(10, 50)))
            content = content.replace("${vol}", str(rng.randint(500, 2000)))
            content = content.replace("${loss}", str(rng.randint(5, 100)))
            content = content.replace("${pct}", f"{rng.uniform(2, 8):.1f}")
            content = content.replace("${bb}", str(rng.randint(5, 50)))
            content = content.replace("${gold}", str(rng.randint(2200, 2800)))

            # Add unique timestamp to URL to avoid dedup collisions
            ts = int(time.time() * 1000) + rng.randint(1, 99999)
            slug = title.lower().replace(" ", "-")[:50]
            items.append({
                "url": f"https://mock-news.example.com/{slug}-{ts}",
                "title": title,
                "raw_content": content,
            })

        return items


class MockRedditMonitor(BaseMonitor):
    """Mock Reddit monitor that generates realistic subreddit posts."""

    async def fetch(self, source: Source) -> list[dict]:
        rng = random.Random(time.time())
        count = rng.randint(1, 2)
        assets = ["BTC", "ETH", "SOL", "XRP", "ADA", "LINK", "AVAX", "DOT"]
        items = []

        for _ in range(count):
            asset = rng.choice(assets)
            template = rng.choice(_REDDIT_TITLES)
            title = template.replace("{asset}", asset)
            title = title.replace("${amount}", str(rng.randint(10, 500)))

            ts = int(time.time() * 1000) + rng.randint(1, 99999)
            subreddit = source.url.split("/")[-1] if "/" in source.url else "CryptoCurrency"
            items.append({
                "url": f"https://reddit.com/r/{subreddit}/comments/mock{ts}",
                "title": title,
                "raw_content": f"Discussion post about {asset} on r/{subreddit}. Score: {rng.randint(50, 2000)}",
            })

        return items


class MockTwitterMonitor(BaseMonitor):
    """Mock Twitter monitor that generates realistic financial tweets."""

    async def fetch(self, source: Source) -> list[dict]:
        rng = random.Random(time.time())
        count = rng.randint(0, 2)
        assets = ["Bitcoin", "Ethereum", "S&P 500", "Gold", "Oil"]
        items = []

        for _ in range(count):
            asset = rng.choice(assets)
            template = rng.choice(_TWITTER_POSTS)
            title = template.replace("{asset}", asset)
            title = title.replace("${price}", f"{rng.randint(1000, 100000):,}")
            title = title.replace("${flow}", str(rng.randint(50, 500)))
            title = title.replace("{support}", f"${rng.randint(50, 90)}K")
            title = title.replace("{resistance}", f"${rng.randint(100, 150)}K")

            ts = int(time.time() * 1000) + rng.randint(1, 99999)
            handle = source.url.split("/")[-1] if "/" in source.url else "CoinDesk"
            items.append({
                "url": f"https://x.com/{handle}/status/{ts}",
                "title": title,
                "raw_content": title,
            })

        return items
