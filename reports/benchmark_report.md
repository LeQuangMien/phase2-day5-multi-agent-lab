# Benchmark Report – Multi-Agent Research System

*Generated: 2026-06-24 11:06*

## Results Summary

| Run | Latency (s) | Cost (USD) | Quality /10 | Notes |
|---|---:|---:|---:|---|
| single-agent | 12.14 | N/A | 5.0 | words=522 citation_coverage=0% errors=0 iterations=1 |
| multi-agent | 31.25 | $0.00066 | 10.0 | words=551 citation_coverage=80% errors=0 iterations=4 |

## Analysis

**Latency:** `multi-agent` took +19.10s (+157.3%) compared to `single-agent`.
**Quality:** `multi-agent` scored +5.0 points higher.

## When to Use Multi-Agent

**Use multi-agent when:**
- The task has clearly separable sub-tasks (research, analysis, writing).
- Quality > latency (multi-agent is slower but more thorough).
- You need auditability: each agent's output is independently inspectable.

**Avoid multi-agent when:**
- The query is simple and one-shot (wastes tokens and latency).
- You have a strict latency SLA (multi-agent adds ≥2× overhead).
- Coordination overhead outweighs specialisation benefit.

## Failure Modes & Fixes

| Mode | Symptom | Fix |
|---|---|---|
| Infinite loop | iteration hits MAX_ITERATIONS | Supervisor must route → done when writer done |
| Agent hallucination | facts not in sources appear in answer | Critic agent + source citation check |
| Search miss | no relevant sources found | Expand mock KB or enable Tavily |
| Timeout | wall-clock > TIMEOUT_SECONDS | Reduce max_sources or increase timeout |

