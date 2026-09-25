"""Fetch podcast + news feeds and keep what is recent and on-topic."""
import calendar
import html
import re
import time
from concurrent.futures import ThreadPoolExecutor

import feedparser
import requests

from . import config

UA = {"User-Agent": "Mozilla/5.0 (compatible; ScrapperBot/1.0)"}


def _clean(text, limit=600):
    text = re.sub(r"<[^>]+>", " ", html.unescape(text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit] + ("…" if len(text) > limit else "")


def _timestamp(entry):
    for key in ("published_parsed", "updated_parsed"):
        if entry.get(key):
            return calendar.timegm(entry[key])
    return None


def _pattern(words):
    parts = [re.escape(w[:-1]) if w.endswith("*") else re.escape(w) + r"s?\b" for w in words]
    return re.compile(r"\b(?:" + "|".join(parts) + ")", re.IGNORECASE)


TOPIC_PATTERNS = {t: _pattern(words) for t, words in config.TOPICS.items()}


def _topics(text):
    return [t for t, pat in TOPIC_PATTERNS.items() if pat.search(text)]


def _fetch(name, url):
    try:
        resp = requests.get(url, headers=UA, timeout=25)
        resp.raise_for_status()
        return name, feedparser.parse(resp.content).entries, None
    except Exception as exc:  # one dead feed must not kill the run
        return name, [], str(exc)


def collect(now=None):
    now = now or time.time()
    feeds = {**config.PODCASTS, **config.NEWS}
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda kv: _fetch(*kv), feeds.items()))

    podcasts, news, errors, seen = [], [], {}, set()
    for name, entries, err in results:
        if err:
            errors[name] = err
            continue
        is_podcast = name in config.PODCASTS
        window = (config.PODCAST_LOOKBACK_DAYS * 86400 if is_podcast
                  else config.NEWS_LOOKBACK_HOURS * 3600)
        for e in entries:
            ts = _timestamp(e)
            if ts is None or now - ts > window:
                continue
            title = _clean(e.get("title"), 200)
            if name.startswith("Google News"):  # "Headline - Outlet"
                title = re.sub(r"\s+-\s+[^-]{2,60}$", "", title)
            key = re.sub(r"\W+", "", title.lower())[:50]
            if key in seen:
                continue
            summary = _clean(e.get("summary") or e.get("description"),
                             1500 if is_podcast else 500)
            topics = _topics(f"{title} {summary}")
            item = {
                "source": name,
                "title": title,
                "link": e.get("link") or next(
                    (l.get("href") for l in e.get("links", []) if l.get("href")), ""),
                "published": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(ts)),
                "ts": ts,
                "summary": summary,
                "topics": topics,
            }
            if is_podcast:
                seen.add(key)
                podcasts.append(item)
            elif topics:
                seen.add(key)
                news.append(item)

    podcasts.sort(key=lambda i: -i["ts"])
    # Rank news by topic breadth, then recency, capping each source for variety.
    news.sort(key=lambda i: (-len(i["topics"]), -i["ts"]))
    per_source, picked = {}, []
    for item in news:
        if per_source.get(item["source"], 0) < config.MAX_PER_SOURCE:
            per_source[item["source"]] = per_source.get(item["source"], 0) + 1
            picked.append(item)
    return {"podcasts": podcasts, "news": picked[:config.MAX_NEWS_ITEMS], "errors": errors}
