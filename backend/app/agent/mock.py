"""Mock implementations for development without API keys."""

import hashlib
import random
import time
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration


def _extract_topic(messages: list[BaseMessage]) -> str:
    """Try to extract the topic from the conversation messages."""
    for m in messages:
        content = m.content if isinstance(m.content, str) else str(m.content)
        for line in content.split("\n"):
            low = line.lower()
            if "topic:" in low:
                return line.split(":", 1)[-1].strip()
    return "the market"


def _topic_seed(topic: str) -> random.Random:
    """Deterministic-per-topic random so the same topic gives consistent data."""
    h = int(hashlib.md5(topic.lower().encode()).hexdigest(), 16)
    return random.Random(h)


# ---------------------------------------------------------------------------
#  Topic knowledge base — provides domain-specific context
# ---------------------------------------------------------------------------

_CRYPTO = {
    "bitcoin", "btc", "ethereum", "eth", "solana", "sol", "cardano", "ada",
    "polygon", "matic", "avalanche", "avax", "chainlink", "link", "dogecoin",
    "doge", "xrp", "ripple", "polkadot", "dot", "litecoin", "ltc", "bnb",
    "cosmos", "atom", "near", "arbitrum", "optimism", "sui", "aptos", "toncoin",
}

_STOCKS = {
    "apple", "aapl", "microsoft", "msft", "google", "googl", "amazon", "amzn",
    "meta", "nvidia", "nvda", "tesla", "tsla", "netflix", "nflx", "amd",
    "intel", "intc", "salesforce", "crm", "adobe", "adbe", "paypal", "pypl",
    "uber", "shopify", "shop", "coinbase", "coin", "palantir", "pltr",
}

_INDICES = {
    "s&p 500", "s&p500", "sp500", "nasdaq", "dow jones", "cac 40", "cac40",
    "dax", "ftse", "nikkei", "hang seng", "russell 2000",
}

_COMMODITIES = {
    "gold", "silver", "oil", "crude oil", "natural gas", "copper", "wheat",
    "corn", "uranium",
}


def _classify(topic: str) -> str:
    t = topic.lower().strip()
    if any(k in t for k in _CRYPTO):
        return "crypto"
    if any(k in t for k in _STOCKS):
        return "stock"
    if any(k in t for k in _INDICES):
        return "index"
    if any(k in t for k in _COMMODITIES):
        return "commodity"
    return "general"


# ---------------------------------------------------------------------------
#  Dynamic question generation
# ---------------------------------------------------------------------------

_QUESTIONS: dict[str, list[list[str]]] = {
    "crypto": [
        [
            "What is {t}'s current price, 24h change, and weekly performance?",
            "How has {t}'s on-chain activity (active addresses, TVL, transaction volume) evolved this week?",
            "What upcoming network upgrades, airdrops, or governance votes could impact {t}?",
            "Which whales or institutions have recently accumulated or sold {t}?",
            "How is {t}'s DeFi ecosystem performing compared to competing L1/L2 chains?",
        ],
        [
            "What are the current funding rates and open interest levels for {t} perpetual futures?",
            "How does {t}'s staking yield compare to alternatives and what is the staking ratio trend?",
            "What recent partnerships or integrations has the {t} ecosystem announced?",
            "What is the developer commit activity trend for {t}'s core repositories?",
            "How are {t} ETF inflows/outflows trending this month?",
        ],
    ],
    "stock": [
        [
            "What were {t}'s most recent quarterly earnings results vs. analyst expectations?",
            "What is {t}'s current valuation (P/E, P/S, EV/EBITDA) relative to sector peers?",
            "What major product launches, acquisitions, or strategic pivots has {t} announced recently?",
            "How are institutional holders adjusting their {t} positions according to latest 13F filings?",
            "What are Wall Street's consensus price target and rating distribution for {t}?",
        ],
        [
            "How has {t}'s revenue growth and margin trajectory evolved over the past 4 quarters?",
            "What insider buying or selling activity has occurred for {t} recently?",
            "How is {t} positioned relative to AI, cloud, or other secular growth trends?",
            "What are the main competitive threats and market share dynamics affecting {t}?",
            "What is {t}'s capital allocation strategy — buybacks, dividends, or R&D investment?",
        ],
    ],
    "index": [
        [
            "What is {t}'s year-to-date performance and how does it compare to other major indices?",
            "Which sectors are leading and lagging within {t} this month?",
            "How are interest rate expectations and Fed policy impacting {t}'s trajectory?",
            "What is the current volatility environment (VIX) and what does it signal for {t}?",
            "Are fund flows into {t}-tracking ETFs accelerating or decelerating?",
        ],
    ],
    "commodity": [
        [
            "What is {t}'s spot price, 30-day trend, and year-to-date return?",
            "How are global supply-demand dynamics shifting for {t}?",
            "What geopolitical factors are currently influencing {t} prices?",
            "How are central bank policies and USD strength affecting {t}?",
            "What are commercial traders' (COT report) net positions signaling for {t}?",
        ],
    ],
    "general": [
        [
            "What is the current market status and recent performance trend for {t}?",
            "What are the key fundamental drivers behind {t}'s valuation right now?",
            "What recent news events or announcements have directly impacted {t}?",
            "How does {t} compare to its closest peers or alternatives?",
            "What are the primary risks and bullish catalysts for {t} over the next quarter?",
        ],
    ],
}

# ---------------------------------------------------------------------------
#  Dynamic fact / summary generation
# ---------------------------------------------------------------------------

def _generate_facts(topic: str, rng: random.Random, category: str) -> list[str]:
    price_change = rng.uniform(-18, 25)
    volume_change = rng.uniform(-30, 80)
    facts_pool: dict[str, list[str]] = {
        "crypto": [
            f"{topic} moved {price_change:+.1f}% over the past 7 days",
            f"Daily active addresses on the {topic} network {'rose' if rng.random() > 0.4 else 'declined'} {abs(rng.uniform(5, 25)):.0f}% week-over-week",
            f"Total Value Locked in {topic} DeFi ecosystem stands at ${rng.uniform(0.5, 45):.1f}B",
            f"{topic} funding rates turned {'positive' if rng.random() > 0.5 else 'negative'}, signaling {'long' if rng.random() > 0.5 else 'short'}-heavy positioning",
            f"A top-10 whale wallet {'accumulated' if rng.random() > 0.4 else 'distributed'} {rng.randint(5, 50)}M worth of {topic}",
            f"{topic} network processed {rng.randint(200, 900)}K transactions in the last 24 hours",
        ],
        "stock": [
            f"{topic} shares {'beat' if rng.random() > 0.4 else 'missed'} earnings estimates by {rng.uniform(1, 15):.1f}%",
            f"Institutional ownership of {topic} {'increased' if rng.random() > 0.5 else 'decreased'} by {rng.uniform(1, 8):.1f}% last quarter",
            f"{topic} announced a ${rng.uniform(0.5, 10):.1f}B {'share buyback program' if rng.random() > 0.5 else 'strategic acquisition'}",
            f"Analyst consensus price target for {topic} implies {rng.uniform(5, 35):.0f}% upside from current levels",
            f"{topic} revenue grew {rng.uniform(5, 40):.0f}% YoY in the latest reported quarter",
        ],
        "index": [
            f"{topic} is {'up' if price_change > 0 else 'down'} {abs(price_change):.1f}% year-to-date",
            f"Market breadth within {topic} is {'improving' if rng.random() > 0.5 else 'narrowing'} — {rng.randint(40, 75)}% of constituents above their 50-DMA",
            f"Inflows into {topic}-tracking ETFs totaled ${rng.uniform(1, 20):.1f}B this month",
            f"The VIX currently sits at {rng.uniform(12, 35):.1f}, {'below' if rng.random() > 0.5 else 'above'} its historical average",
        ],
        "commodity": [
            f"{topic} spot price moved {price_change:+.1f}% over the past month",
            f"Global {topic} inventories {'fell' if rng.random() > 0.5 else 'rose'} to {rng.uniform(1, 8):.1f}-month {'lows' if rng.random() > 0.5 else 'highs'}",
            f"Speculative net longs on {topic} {'increased' if rng.random() > 0.5 else 'decreased'} {rng.uniform(5, 30):.0f}% per latest COT data",
            f"Major {'producer' if rng.random() > 0.5 else 'consumer'} nations signaled policy changes affecting {topic} supply",
        ],
        "general": [
            f"{topic} saw trading volume change {volume_change:+.0f}% compared to the prior period",
            f"Sentiment on {topic} shifted {'bullish' if rng.random() > 0.5 else 'cautious'} across social media and analyst notes",
            f"A key regulatory development could {'boost' if rng.random() > 0.5 else 'constrain'} {topic}'s growth trajectory",
            f"Multiple analysts revised their {topic} outlook {'upward' if rng.random() > 0.5 else 'downward'} this week",
        ],
    }
    pool = facts_pool.get(category, facts_pool["general"])
    rng.shuffle(pool)
    return pool[:4]


def _generate_summary(topic: str, rng: random.Random, category: str) -> str:
    facts = _generate_facts(topic, rng, category)
    return "\n".join(f"- {f}" for f in facts)


# ---------------------------------------------------------------------------
#  Mock LLM
# ---------------------------------------------------------------------------

class MockChatModel(BaseChatModel):
    """Mock LLM that returns realistic, topic-aware financial analysis."""

    model_name: str = "mock-gpt-4o-mini"

    @property
    def _llm_type(self) -> str:
        return "mock"

    def _generate(self, messages: list[BaseMessage], stop=None, **kwargs) -> ChatResult:
        prompt = messages[-1].content if messages else ""
        topic = _extract_topic(messages)
        category = _classify(topic)
        rng = _topic_seed(topic + prompt[:20])  # vary per prompt type too

        if "sub-questions" in prompt.lower() or "decompose" in prompt.lower():
            templates = _QUESTIONS.get(category, _QUESTIONS["general"])
            template = rng.choice(templates)
            questions = [q.format(t=topic) for q in template]
            # pick 3-5 random questions
            k = rng.randint(3, min(5, len(questions)))
            chosen = rng.sample(questions, k)
            content = "\n".join(f"{i+1}. {q}" for i, q in enumerate(chosen))

        elif "summarize" in prompt.lower() or "filter" in prompt.lower():
            content = _generate_summary(topic, rng, category)

        elif "sentiment" in prompt.lower() or "analy" in prompt.lower():
            sentiments = ["bullish", "bullish", "bullish", "neutral", "bearish"]
            s = rng.choice(sentiments)
            score = {"bullish": round(rng.uniform(0.65, 0.92), 2),
                     "bearish": round(rng.uniform(0.15, 0.40), 2),
                     "neutral": round(rng.uniform(0.45, 0.60), 2)}[s]
            facts = _generate_facts(topic, rng, category)
            facts_str = "\n".join(f"- {f}" for f in facts)
            content = (
                f"SENTIMENT: {s}\n"
                f"SCORE: {score}\n"
                f"KEY_FACTS:\n{facts_str}"
            )

        elif "report" in prompt.lower() or "write" in prompt.lower():
            content = _generate_mock_report(topic, category, rng)

        else:
            content = "This is a mock response for development purposes."

        time.sleep(0.3)
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])


# ---------------------------------------------------------------------------
#  Mock Search Client
# ---------------------------------------------------------------------------

class MockTavilyClient:
    """Mock search client that returns topic-aware financial news results."""

    def search(self, query: str, max_results: int = 5, **kwargs) -> dict:
        time.sleep(0.2)
        rng = _topic_seed(query)

        # Extract a clean topic name from the query (which may be a full question)
        topic = query
        for kw in _CRYPTO | _STOCKS | _INDICES | _COMMODITIES:
            if kw.lower() in query.lower():
                topic = kw.title()
                break
        slug = topic.lower().replace(" ", "-").replace("&", "and")

        price_chg = rng.uniform(-12, 18)
        sources = ["Reuters", "Bloomberg", "CoinDesk", "CNBC", "Financial Times",
                    "The Block", "MarketWatch", "Barron's", "Decrypt", "TechCrunch"]
        rng.shuffle(sources)

        base_results = [
            {
                "title": f"{topic} {'Surges' if price_chg > 5 else 'Drops' if price_chg < -5 else 'Holds Steady'} Amid Shifting Market Sentiment — {sources[0]}",
                "url": f"https://{sources[0].lower().replace(' ', '')}.com/markets/{slug}-update-march-2026",
                "content": (
                    f"{topic} has {'gained' if price_chg > 0 else 'lost'} {abs(price_chg):.1f}% over the past week. "
                    f"Trading volume spiked {rng.uniform(15, 60):.0f}% as {'buyers' if price_chg > 0 else 'sellers'} "
                    f"dominated. Analysts point to {'improving fundamentals' if price_chg > 0 else 'profit-taking'} "
                    f"as the key driver."
                ),
            },
            {
                "title": f"What's Next for {topic}? Key Levels and Catalysts to Watch — {sources[1]}",
                "url": f"https://{sources[1].lower().replace(' ', '')}.com/analysis/{slug}-outlook",
                "content": (
                    f"Multiple factors are converging for {topic}: "
                    f"{'favorable macro conditions' if rng.random() > 0.5 else 'shifting regulatory landscape'}, "
                    f"{'growing institutional adoption' if rng.random() > 0.5 else 'retail momentum building'}, "
                    f"and {'strong technical setup' if rng.random() > 0.5 else 'improving fundamentals'}."
                ),
            },
            {
                "title": f"{topic}: Institutional Flows {'Accelerate' if rng.random() > 0.5 else 'Slow'} as Q2 Begins — {sources[2]}",
                "url": f"https://{sources[2].lower().replace(' ', '')}.com/institutional/{slug}-flows-q2-2026",
                "content": (
                    f"Our Q2 outlook for {topic} incorporates {rng.randint(15, 40)} data sources. "
                    f"Key finding: {'upside potential outweighs downside risks' if rng.random() > 0.4 else 'risk-reward appears balanced'}. "
                    f"Primary catalyst: {'expansion into new markets' if rng.random() > 0.5 else 'margin improvement trajectory'}."
                ),
            },
        ]
        return {"results": base_results[:max_results]}


# ---------------------------------------------------------------------------
#  Mock report generation
# ---------------------------------------------------------------------------

def _generate_mock_report(topic: str, category: str, rng: random.Random) -> str:
    price_chg = rng.uniform(-15, 25)
    vol_chg = rng.uniform(10, 60)
    direction = "up" if price_chg > 0 else "down"
    sentiment = rng.choice(["cautiously optimistic", "mixed but leaning bullish", "neutral with upside bias", "bearish near-term but constructive long-term"])

    if category == "crypto":
        overview = (
            f"{topic} is currently trading {'higher' if price_chg > 0 else 'lower'}, "
            f"with a {abs(price_chg):.1f}% move over the past 7 days. "
            f"On-chain metrics show {'increasing' if rng.random() > 0.4 else 'stable'} network activity, "
            f"with daily active addresses {'rising' if rng.random() > 0.5 else 'holding steady'}. "
            f"The DeFi ecosystem built on {topic} has seen TVL {'grow' if rng.random() > 0.5 else 'consolidate'} "
            f"around ${rng.uniform(1, 40):.1f}B."
        )
        developments = (
            f"1. **Network Activity**: {topic}'s daily transactions reached {rng.randint(200, 900)}K, "
            f"{'a new monthly high' if rng.random() > 0.5 else 'consistent with recent averages'}.\n"
            f"2. **Ecosystem Growth**: {rng.randint(5, 30)} new protocols launched on {topic} this month, "
            f"expanding the DeFi and NFT landscape.\n"
            f"3. **Institutional Interest**: {'ETF inflows' if rng.random() > 0.5 else 'Institutional funds'} "
            f"{'accelerated' if rng.random() > 0.5 else 'remained steady'} with "
            f"${rng.uniform(50, 500):.0f}M in weekly {'inflows' if rng.random() > 0.5 else 'allocations'}.\n"
            f"4. **Upcoming Catalyst**: A major {'network upgrade' if rng.random() > 0.5 else 'governance vote'} "
            f"is scheduled for {'next week' if rng.random() > 0.5 else 'early next month'}, "
            f"which could significantly impact {topic}'s trajectory."
        )
    elif category == "stock":
        overview = (
            f"{topic} shares moved {price_chg:+.1f}% this period following "
            f"{'better-than-expected' if rng.random() > 0.4 else 'mixed'} quarterly results. "
            f"Revenue {'beat' if rng.random() > 0.5 else 'met'} consensus estimates, "
            f"while margins {'expanded' if rng.random() > 0.5 else 'compressed slightly'}. "
            f"The stock currently trades at {rng.uniform(15, 45):.1f}x forward earnings."
        )
        developments = (
            f"1. **Earnings**: {topic} reported revenue of ${rng.uniform(5, 100):.1f}B, "
            f"{'beating' if rng.random() > 0.5 else 'in-line with'} consensus by {rng.uniform(1, 8):.1f}%.\n"
            f"2. **Strategic Moves**: Management announced {'a major acquisition' if rng.random() > 0.5 else 'expanded buyback authorization'} "
            f"worth ${rng.uniform(1, 15):.1f}B.\n"
            f"3. **Competitive Position**: {topic} {'gained' if rng.random() > 0.5 else 'maintained'} "
            f"market share in its core segments.\n"
            f"4. **Guidance**: Forward guidance was {'raised' if rng.random() > 0.5 else 'reaffirmed'}, "
            f"implying {rng.uniform(8, 30):.0f}% YoY growth for the next quarter."
        )
    else:
        overview = (
            f"{topic} has moved {price_chg:+.1f}% over the recent period, "
            f"with trading volume {'surging' if vol_chg > 30 else 'increasing'} {vol_chg:.0f}%. "
            f"Market participants are responding to a combination of "
            f"{'macro developments' if rng.random() > 0.5 else 'sector-specific catalysts'} "
            f"and {'shifting sentiment' if rng.random() > 0.5 else 'technical breakout signals'}."
        )
        developments = (
            f"1. **Market Dynamics**: {topic} volume {'surged' if vol_chg > 30 else 'rose'} {vol_chg:.0f}%, "
            f"reflecting heightened interest.\n"
            f"2. **Macro Backdrop**: {'Dovish central bank signals' if rng.random() > 0.5 else 'Inflation data'} "
            f"{'supported' if rng.random() > 0.5 else 'weighed on'} sentiment.\n"
            f"3. **Flows**: Institutional {'inflows' if rng.random() > 0.5 else 'positioning'} "
            f"{'accelerated' if rng.random() > 0.5 else 'remained constructive'}.\n"
            f"4. **Outlook**: Key catalysts ahead include "
            f"{'upcoming earnings season' if rng.random() > 0.5 else 'policy decisions'} "
            f"and {'geopolitical developments' if rng.random() > 0.5 else 'technical levels being tested'}."
        )

    return f"""# Market Intelligence Report: {topic}

## Executive Summary

This report analyzes **{topic}** using data from multiple sources including price action, volume analysis, on-chain/fundamental data, and sentiment indicators. Overall market sentiment is **{sentiment}**.

## Current Market Overview

{overview}

Key levels to watch:
- **Support**: {rng.uniform(0.85, 0.95):.0%} of current price (recent consolidation zone)
- **Resistance**: {rng.uniform(1.05, 1.20):.0%} of current price (previous swing high)

## Sentiment Analysis

Market sentiment for {topic} is **{sentiment}** based on our multi-source analysis:

| Indicator | Signal |
|-----------|--------|
| Social Media Sentiment | {'Positive' if rng.random() > 0.4 else 'Mixed'} |
| Institutional Flow | {'Accumulation' if rng.random() > 0.4 else 'Neutral'} |
| Technical Indicators | {'Bullish' if price_chg > 5 else 'Bearish' if price_chg < -5 else 'Mixed'} |
| News Sentiment | {'Positive' if rng.random() > 0.4 else 'Slightly cautious'} |

## Key Developments

{developments}

## Risk Factors

- {'Regulatory uncertainty' if rng.random() > 0.5 else 'Policy changes'} could create short-term volatility
- {'Macro deterioration' if rng.random() > 0.5 else 'Rising interest rates'} may pressure valuations
- {'Profit-taking at resistance levels' if rng.random() > 0.5 else 'Technical breakdown below support'} is possible
- {'Competition intensifying' if rng.random() > 0.5 else 'Execution risks'} remain a concern

## Outlook

The near-term outlook for {topic} is **{'moderately positive' if price_chg > 0 else 'cautious with recovery potential'}**. Key catalysts in the coming weeks could drive significant price action. Position sizing should account for {'elevated' if abs(price_chg) > 10 else 'moderate'} volatility.

---
*Report generated by AlphaWatch AI Agent — Mock Mode*
"""
