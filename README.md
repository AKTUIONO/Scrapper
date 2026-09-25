# Scrapper: daily frontier-tech and impact scout

Every morning this agent:

1. **Scrapes** the latest episodes of **Moonshots with Peter Diamandis** and **The Joe Rogan Experience**, plus about 17 news feeds covering AI, superintelligence, biotech, longevity, quantum, energy/space and brain-computer interfaces (`scrapper/config.py`).
2. **Filters** the news to on-topic stories from the last 36 hours and the podcasts to the last 7 days. It removes duplicates and limits each source so no single feed dominates.
3. **Generates 3 new social-entrepreneurship ideas** with Claude. Each idea is grounded in that day's signals and cites them. It is checked against every earlier idea (`data/ideas_history.json`) so ideas don't repeat.
4. **Writes the morning briefing** to `briefings/YYYY-MM-DD.md` (and `briefings/LATEST.md`), then **opens a GitHub issue** with it. GitHub emails that issue to you.

## Setup (one time)

1. In the repo, go to **Settings → Secrets and variables → Actions → New repository secret**. Name it `ANTHROPIC_API_KEY` and paste a key from https://console.anthropic.com. Without the key, the briefing still runs but has no ideas section.
2. Click **Watch → All Activity** on the repo so the daily issue arrives in your email.
3. To test right away: **Actions → Daily frontier-tech briefing → Run workflow**.

The workflow runs daily at 11:05 UTC (7:05 AM Eastern). Change the `cron` line in `.github/workflows/daily-briefing.yml` to use a different time.

## Run locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...        # optional
python -m scrapper run              # scrape → ideas → briefing
python -m scrapper collect          # scrape only
python -m scrapper render           # re-render from data/<date>/ (digest.json + ideas.json)
```

To add or remove sources and keywords, edit `scrapper/config.py`. To change the mission focus for the ideas, edit `SYSTEM` in `scrapper/ideas.py`.
