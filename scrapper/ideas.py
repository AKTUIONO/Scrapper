"""Turn the day's signals into novel social-entrepreneurship ideas with Claude."""
import json
from typing import List

from pydantic import BaseModel

MODEL = "claude-opus-5"

SYSTEM = """You are the daily idea scout for a faith-driven impact investing team \
(Tribe of Judah Elite Financial Team; LP in emerging-tech ventures) focused on AI, \
superintelligence, biotech, longevity, quantum, and the infrastructure, hardware, \
software and education that shape the future. Their aim is ventures that do real good \
for humanity while being financially sustainable enough to reinvest.

From today's signals, propose genuinely new social-entrepreneurship ideas: things almost \
nobody is building yet, that combine a fresh technical capability with an underserved \
human need (health equity, education, jobs displaced by AI, aging populations, access \
for low-income or rural communities, faith and family communities, the Global South). \
Avoid generic ideas ("AI tutor app", "telehealth platform") and anything in the \
previously proposed list. Ground every idea in specific signals from today and cite them. \
Be honest about risks and why it might not already exist."""


class Idea(BaseModel):
    title: str
    one_liner: str
    problem: str
    solution: str
    why_now: str
    why_nobody_is_doing_it: str
    social_impact: str
    business_model: str
    first_step_this_week: str
    topics: List[str]
    sources: List[str]


class Briefing(BaseModel):
    headline_summary: str
    top_signals: List[str]
    ideas: List[Idea]


def _signals_text(digest):
    lines = ["## Podcast episodes (last 7 days)"]
    for p in digest["podcasts"]:
        lines.append(f"- [{p['source']}] {p['title']} ({p['published']}) {p['link']}\n  {p['summary']}")
    lines.append("\n## News (last 36 hours)")
    for n in digest["news"]:
        lines.append(f"- [{n['source']}] {n['title']} ({', '.join(n['topics'])}) {n['link']}\n  {n['summary']}")
    return "\n".join(lines)


def generate(digest, history, n_ideas=3):
    import anthropic

    past = "\n".join(f"- {t}" for t in history[-150:]) or "(none yet)"
    prompt = (
        f"Today's signals:\n\n{_signals_text(digest)}\n\n"
        f"Previously proposed ideas (do not repeat or lightly reword):\n{past}\n\n"
        f"Write a 3-4 sentence headline_summary of what matters today, 5-8 top_signals "
        f"(one line each, name the source), and exactly {n_ideas} ideas. In each idea's "
        f"sources list the URLs of the signals it builds on."
    )
    client = anthropic.Anthropic()
    response = client.messages.parse(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
        output_format=Briefing,
    )
    if response.stop_reason == "refusal" or response.parsed_output is None:
        raise RuntimeError(f"Claude returned no briefing (stop_reason={response.stop_reason})")
    return json.loads(response.parsed_output.model_dump_json())
