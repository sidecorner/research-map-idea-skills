# research-map-idea-skills — Local Project Instructions

## Local Skill

This project contains a local-only skill for proximity communication (すれ違い通信) idea research.

**Skill:** `proximity-communication-idea-research`
**Skill file:** `SKILL.md` (in this directory)

When working in this project, load and follow `SKILL.md` whenever the user asks to:
- Research product ideas for proximity or encounter communication apps
- Investigate すれ違い通信 features or StreetPass-style mechanics
- Find user pain points in location-based social, Bluetooth, or NFC-related communities
- Generate or evaluate niche app ideas for small-team development
- Run research with scoring (実現可能性, 開発期間, 収益性, 競合優位性, 小規模開発適性)

## Project Structure

```
research-map-idea-skills/
├── CLAUDE.md               ← this file (local skill registration)
├── SKILL.md                ← skill definition (load when triggered)
├── scripts/
│   ├── fetch_reddit_proximity.py  ← Reddit data collection (proximity-adapted)
│   └── fetch_hn.py                ← HN data collection (use with --queries override)
├── references/
│   ├── subreddits.md       ← Subreddit list with rationale
│   ├── hn_queries.md       ← HN query list with notes
│   ├── scoring_rubric.md   ← 5-dimension scoring guide
│   └── report_template.md  ← Report output template
└── reports/
    └── {year}/
        └── yyyy-mm-dd/
            └── HHMMSS.md   ← Generated research reports
```

## Scope

This skill is **scoped to this directory only**. Do not apply it in other projects.
