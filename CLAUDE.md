# research-map-idea-skills — Local Project Instructions

## Local Skills

This project contains two local-only research skills. Load the appropriate skill based on the user's request.

---

### Skill 1: `proximity-communication-idea-research`

**Skill file:** `SKILL.md`

Load and follow `SKILL.md` whenever the user asks to:
- Research product ideas for proximity or encounter communication apps
- Investigate すれ違い通信 features or StreetPass-style mechanics
- Find user pain points in location-based social, Bluetooth, NFC, or GPS-based communities
- Generate or evaluate niche app ideas involving physical proximity between people
- Run research with scoring (実現可能性, 開発期間, 収益性, 競合優位性, 小規模開発適性)

---

### Skill 2: `light-information-exchange-idea-research`

**Skill file:** `SKILL_light_exchange.md`

Load and follow `SKILL_light_exchange.md` whenever the user asks to:
- Research product ideas for casual, lightweight, or low-friction information sharing
- Explore anonymous sharing, ephemeral notes, hyperlocal bulletin boards, or micro-social concepts
- Find alternatives to heavy social media for simple, quick information exchange
- Investigate user pain points around peer Q&A, community tips, or ambient knowledge discovery
- Generate or evaluate niche app ideas in the lightweight/casual info-sharing space

---

### When the request spans both themes

If the user asks about an app that combines **proximity** with **lightweight information exchange**
(e.g., "leave an anonymous note for people who walk past here"), treat that as a joint session:
load both skill files and apply the union of their research approaches and idea patterns.

---

## Project Structure

```
research-map-idea-skills/
├── CLAUDE.md                              ← this file
├── SKILL.md                               ← Skill 1: proximity communication
├── SKILL_light_exchange.md                ← Skill 2: light information exchange
├── README.md
│
├── scripts/
│   ├── fetch_reddit_proximity.py          ← Reddit (proximity)
│   ├── fetch_hn_proximity.py              ← HN (proximity) --rolling 対応
│   ├── fetch_qiita_proximity.py           ← Qiita (proximity) --rolling 対応
│   ├── fetch_reddit_light_exchange.py     ← Reddit (light exchange)
│   ├── fetch_hn_light_exchange.py         ← HN (light exchange) --rolling 対応
│   ├── fetch_qiita_light_exchange.py      ← Qiita (light exchange) --rolling 対応
│   ├── fetch_reddit.py                    ← 汎用 Reddit スクリプト（元ファイル）
│   └── fetch_hn.py                        ← 汎用 HN スクリプト（元ファイル）
│
├── references/
│   ├── subreddits.md                      ← Skill 1 subreddit list
│   ├── hn_queries.md                      ← Skill 1 HN queries
│   ├── qiita_queries_proximity.md         ← Skill 1 Qiita queries
│   ├── light_exchange_subreddits.md       ← Skill 2 subreddit list
│   ├── light_exchange_hn_queries.md       ← Skill 2 HN queries
│   ├── qiita_queries_light_exchange.md    ← Skill 2 Qiita queries
│   ├── scoring_rubric.md                  ← 共通: 5軸スコアリング基準
│   └── report_template.md                 ← 共通: レポートテンプレート
│
└── reports/
    └── {year}/
        └── yyyy-mm-dd/
            └── HHMMSS.md
```

## Date Range Logic

- **Current year (or no year specified):** Use rolling 12-month window (`--rolling` flag). Example: if today is 2026-03-15, collect from 2025-03-15 to 2026-03-15.
- **Past year:** Use full calendar year (`--year YYYY`). Example: `--year 2025` collects 2025-01-01 to 2025-12-31.

## Scope

Both skills are **scoped to this directory only**. Do not apply them in other projects.
