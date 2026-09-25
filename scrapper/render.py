"""Render the digest + ideas as a Markdown morning briefing."""


def render(date, digest, briefing=None, note=None):
    out = [f"# Frontier Tech & Impact Briefing — {date}", ""]
    if note:
        out += [f"> ⚠️ {note}", ""]
    if briefing:
        out += ["## Today in one minute", "", briefing["headline_summary"], ""]
        out += ["## Top signals", ""] + [f"- {s}" for s in briefing["top_signals"]] + [""]
        out += ["## New social-entrepreneurship ideas", ""]
        for i, idea in enumerate(briefing["ideas"], 1):
            out += [
                f"### {i}. {idea['title']}",
                f"_{idea['one_liner']}_  ",
                f"**Topics:** {', '.join(idea['topics'])}",
                "",
                f"- **Problem:** {idea['problem']}",
                f"- **Solution:** {idea['solution']}",
                f"- **Why now:** {idea['why_now']}",
                f"- **Why nobody is doing it yet:** {idea['why_nobody_is_doing_it']}",
                f"- **Social impact:** {idea['social_impact']}",
                f"- **Business model:** {idea['business_model']}",
                f"- **First step this week:** {idea['first_step_this_week']}",
                "- **Built on:** " + " ".join(
                    f"[{n}]({u})" for n, u in enumerate(idea["sources"], 1)),
                "",
            ]
    else:
        out += ["_Ideas not generated yet (no ANTHROPIC_API_KEY). Signals below._", ""]

    out += ["## Podcasts this week", ""]
    for p in digest["podcasts"] or []:
        out.append(f"- **{p['source']}** — [{p['title']}]({p['link']}) · {p['published']}")
    if not digest["podcasts"]:
        out.append("- No new episodes in the last 7 days.")

    out += ["", "## News radar", ""]
    for n in digest["news"]:
        out.append(f"- [{n['title']}]({n['link']}) — {n['source']} · _{', '.join(n['topics'])}_")

    if digest.get("errors"):
        out += ["", "<details><summary>Feeds that failed today</summary>", ""]
        out += [f"- {k}: {v}" for k, v in digest["errors"].items()]
        out += ["", "</details>"]
    return "\n".join(out) + "\n"
