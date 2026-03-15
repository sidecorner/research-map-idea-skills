# research-map-idea-skills — Local Project Instructions

## Local Skill

This project contains one local research skill.

**Skill file:** `SKILL.md`

Load and follow `SKILL.md` whenever the user asks to:
- Research product ideas for proximity or encounter communication apps (すれ違い通信)
- Investigate StreetPass-style mechanics, Bluetooth/NFC/GPS-based social features
- Research product ideas for casual, lightweight, or low-friction information sharing
- Explore anonymous sharing, ephemeral notes, hyperlocal bulletin boards, or micro-social concepts
- Find user pain points in location-based, anonymous, or community-sharing apps
- Generate or evaluate niche app ideas with scoring (実現可能性, 開発期間, 収益性, 競合優位性, 小規模開発適性)

---

## Project Structure

```
research-map-idea-skills/
├── CLAUDE.md                    ← this file
├── SKILL.md                     ← unified research skill
├── README.md
│
├── scripts/
│   ├── fetch_reddit.py          ← Reddit data collection
│   ├── fetch_hn.py              ← HN data collection (--rolling 対応)
│   └── fetch_qiita.py           ← Qiita data collection (--rolling 対応)
│
├── references/
│   ├── analysis_guide.md        ← データ分析・クロスリファレンスガイド
│   ├── idea_patterns.md         ← アイデアパターン・制約適用ガイド
│   ├── scoring_rubric.md        ← 5軸スコアリング基準
│   └── report_template.md       ← レポートテンプレート
│
└── reports/
    └── {year}/
        └── yyyymmdd/            ← ダッシュなし（例: 20260315）
            └── hhmmss.md        ← 24時間・セパレータなし（例: 214710.md）
```

## Date Range Logic

- **Current year (or no year specified):** Use rolling 12-month window (`--rolling` flag for HN/Qiita). Example: if today is 2026-03-15, collect from 2025-03-15 to 2026-03-15.
- **Past year:** Use full calendar year (`--year YYYY`). Example: `--year 2025` collects 2025-01-01 to 2025-12-31.
- **Reddit:** Always pass `--year {year}` (no `--rolling` flag). Reddit's API returns the past 12 months automatically when the year is current.

## Post-Execution Self-Review (mandatory)

After every skill run, always execute **Step 5** defined in `SKILL.md`:

- Review scripts for bugs or errors encountered during the run
- Check if queries/keywords need updating based on new terminology in the data
- Fix any skill instruction gaps or template inconsistencies
- Update `README.md` if the user-facing description is now inaccurate
- Report changes in Japanese at the end of the response (2–3 bullets, no separate file)

This applies even if the user does not explicitly ask for it.

## Scope

This skill is **scoped to this directory only**. Do not apply it in other projects.
