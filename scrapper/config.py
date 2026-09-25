"""Sources and topic keywords for the daily frontier-tech scan."""

# Podcasts: every recent episode is kept (they are the priority signal).
PODCASTS = {
    "Moonshots with Peter Diamandis": "https://feeds.megaphone.fm/DVVTS2890392624",
    "The Joe Rogan Experience": "https://feeds.megaphone.fm/GLT1412515089",
}

# News feeds: items are kept only if they match a topic keyword.
NEWS = {
    "Diamandis Blog": "https://www.diamandis.com/blog/rss.xml",
    "Singularity Hub": "https://singularityhub.com/feed/",
    "MIT Technology Review": "https://www.technologyreview.com/feed/",
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "OpenAI News": "https://openai.com/news/rss.xml",
    "Hacker News Best": "https://hnrss.org/best",
    "STAT News": "https://www.statnews.com/feed/",
    "Lifespan.io": "https://www.lifespan.io/feed/",
    "The Quantum Insider": "https://thequantuminsider.com/feed/",
    "Quanta Magazine": "https://www.quantamagazine.org/feed/",
    "ScienceDaily Tech": "https://www.sciencedaily.com/rss/top/technology.xml",
    "NextBigFuture": "https://www.nextbigfuture.com/feed",
    "Google News: AI": "https://news.google.com/rss/search?q=%22artificial+intelligence%22+OR+superintelligence+when:1d&hl=en-US&gl=US&ceid=US:en",
    "Google News: Longevity": "https://news.google.com/rss/search?q=longevity+OR+%22anti-aging%22+OR+senolytic+when:2d&hl=en-US&gl=US&ceid=US:en",
    "Google News: Quantum": "https://news.google.com/rss/search?q=%22quantum+computing%22+when:2d&hl=en-US&gl=US&ceid=US:en",
    "Google News: Biotech": "https://news.google.com/rss/search?q=biotech+OR+CRISPR+OR+%22gene+therapy%22+when:2d&hl=en-US&gl=US&ceid=US:en",
}

# Whole-word match (plural "s" allowed); a trailing * means prefix match.
TOPICS = {
    "AI": ["artificial intelligence", "ai", "a.i.", "llm", "gpt*", "claude", "gemini",
           "openai", "anthropic", "deepmind", "neural", "machine learning", "chatbot",
           "agentic", "ai agent", "robot*", "humanoid", "nvidia", "data center", "datacenter"],
    "Superintelligence": ["superintelligen*", "agi", "asi", "singularity", "alignment",
                          "frontier model", "ai safety"],
    "Biotech": ["biotech*", "crispr", "gene", "gene therap*", "genom*", "protein", "drug",
                "fda", "clinical trial", "cell therap*", "mrna", "synthetic biology",
                "vaccine", "cancer"],
    "Longevity": ["longevity", "aging", "ageing", "lifespan", "healthspan", "senolytic",
                  "rejuvenat*", "epigenetic", "biological age"],
    "Quantum": ["quantum", "qubit"],
    "Energy & Space": ["fusion", "batter*", "solar", "nuclear", "spacex", "starship", "orbit*"],
    "Brain-Computer": ["neuralink", "brain-computer", "bci", "neurotech*"],
}

PODCAST_LOOKBACK_DAYS = 7
NEWS_LOOKBACK_HOURS = 36
MAX_NEWS_ITEMS = 60
MAX_PER_SOURCE = 6
