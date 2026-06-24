"""Benchmark report rendering."""

from datetime import datetime

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to a rich markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# Benchmark Report – Multi-Agent Research System",
        "",
        f"*Generated: {now}*",
        "",
        "## Results Summary",
        "",
        "| Run | Latency (s) | Cost (USD) | Quality /10 | Notes |",
        "|---|---:|---:|---:|---|",
    ]
    for item in metrics:
        cost = "N/A" if item.estimated_cost_usd is None else f"${item.estimated_cost_usd:.5f}"
        quality = "N/A" if item.quality_score is None else f"{item.quality_score:.1f}"
        lines.append(
            f"| {item.run_name} | {item.latency_seconds:.2f} | {cost} | {quality} | {item.notes} |"
        )

    lines += [
        "",
        "## Analysis",
        "",
    ]

    if len(metrics) == 2:
        a, b = metrics[0], metrics[1]
        latency_delta = b.latency_seconds - a.latency_seconds
        latency_pct = (latency_delta / a.latency_seconds) * 100 if a.latency_seconds else 0

        quality_delta: float | None = None
        if a.quality_score is not None and b.quality_score is not None:
            quality_delta = b.quality_score - a.quality_score

        lines.append(f"**Latency:** `{b.run_name}` took {latency_delta:+.2f}s "
                     f"({latency_pct:+.1f}%) compared to `{a.run_name}`.")

        if quality_delta is not None:
            direction = "higher" if quality_delta > 0 else "lower"
            lines.append(f"**Quality:** `{b.run_name}` scored {quality_delta:+.1f} points {direction}.")

        lines += [
            "",
            "## When to Use Multi-Agent",
            "",
            "**Use multi-agent when:**",
            "- The task has clearly separable sub-tasks (research, analysis, writing).",
            "- Quality > latency (multi-agent is slower but more thorough).",
            "- You need auditability: each agent's output is independently inspectable.",
            "",
            "**Avoid multi-agent when:**",
            "- The query is simple and one-shot (wastes tokens and latency).",
            "- You have a strict latency SLA (multi-agent adds ≥2× overhead).",
            "- Coordination overhead outweighs specialisation benefit.",
            "",
        ]

    lines += [
        "## Failure Modes & Fixes",
        "",
        "| Mode | Symptom | Fix |",
        "|---|---|---|",
        "| Infinite loop | iteration hits MAX_ITERATIONS | Supervisor must route → done when writer done |",
        "| Agent hallucination | facts not in sources appear in answer | Critic agent + source citation check |",
        "| Search miss | no relevant sources found | Expand mock KB or enable Tavily |",
        "| Timeout | wall-clock > TIMEOUT_SECONDS | Reduce max_sources or increase timeout |",
        "",
    ]

    return "\n".join(lines) + "\n"