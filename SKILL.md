---
name: idea-research
description: >
  Research and generate niche product ideas for apps or web services built around
  proximity/encounter communication (すれ違い通信) and lightweight information exchange —
  such as GPS-based location unlock mechanics, geofence-triggered content, location-based
  encounters, StreetPass-style mechanics, ephemeral local notes, anonymous peer Q&A, and
  hyperlocal bulletin boards. Pulls real user pain points from Reddit, Hacker News, and
  Qiita, then synthesizes actionable ideas with feasibility scoring. NFC is excluded.

  ALWAYS use this skill when the user wants to:
  - Research product ideas involving proximity communication, すれ違い通信, or encounter features
  - Research product ideas for lightweight, casual, or low-friction information sharing
  - Discover underserved niches in location-based, Bluetooth-based, or anonymous social apps
  - Generate scored idea candidates for a small-team or indie developer to build
---

# Idea Research Skill

---

## Step 0: Confirm Target Year and Constraints (ask in Japanese)

Ask the user two questions in a single message:

> 「以下の2点を教えてください。
>
> **① 調査対象の年号**（例：2026）
> 　指定がなければ今年（{current_year}）で進めます。
>
> **② 優先したい条件・制約**（任意）
> 　例：「iOS向け」「BLEのみ」「日本市場」「ゲーム系」「B2B SaaS」「ソロ開発」「NFC限定」「マッチング系は除く」「匿名性重視」「Google Maps/Mapbox使用」など。
> 　なければ「なし」か空欄で構いません。」

Save `{year}` and `{constraints}`. Constraints guide idea generation (Step 3) but do **not** narrow data collection.

**Date range logic:**

| Condition | Range | Flag |
|-----------|-------|------|
| `{year}` == current year | rolling 12 months (today − 1 year → today) | `--rolling` for HN/Qiita |
| `{year}` is a past year | {year}-01-01 → {year}-12-31 | `--year {year}` for all |

---

## Step 1: Collect Data

Run all scripts from the project root (`research-map-idea-skills/`).

> **Reddit:** always use `--year {year}`, never `--rolling`.
> **Indie Hackers:** always use `--rolling` for current year; use `--year {year}` for past years.

```bash
# Reddit
python scripts/fetch_reddit.py --year {year} --limit 30 --output /tmp/reddit_{year}.json

# Hacker News (rolling / current year)
python scripts/fetch_hn.py --rolling --min-points 5 --output /tmp/hn_rolling.json

# Hacker News (past year)
python scripts/fetch_hn.py --year {year} --min-points 5 --output /tmp/hn_{year}.json

# Qiita (rolling / current year)
python scripts/fetch_qiita.py --rolling --output /tmp/qiita_rolling.json

# Qiita (past year)
python scripts/fetch_qiita.py --year {year} --output /tmp/qiita_{year}.json

# Indie Hackers (rolling / current year)
python scripts/fetch_indiehackers.py --rolling --output /tmp/ih_rolling.json

# Indie Hackers (past year)
python scripts/fetch_indiehackers.py --year {year} --output /tmp/ih_{year}.json
```

If HN yields fewer than 10 posts, supplement with the previous year (`--year {year-1} --min-points 10`).

Qiita token is auto-read from `QIITA_TOKEN` env var, `~/.config/qiita/token`, or `.env`. If `rate_limited: true`, partial results are still usable — note it in the report.

---

## Step 2: Analyze the Data

Read all output files. See `references/analysis_guide.md` for what to look for in each source and how to cross-reference patterns across Reddit, HN, and Qiita.

---

## Step 3: Generate Ideas

Propose **3–5 product ideas**. See `references/idea_patterns.md` for good idea patterns and constraint adjustment guidance.

Score each idea using `references/scoring_rubric.md`.

---

## Step 4: Write the Report

Follow the template in `references/report_template.md`.

**File path:** `reports/{year}/{yyyymmdd}/{hhmmss}.md`
- Date: no dashes (e.g. `20260315`)
- Time: 24-hour, no separators (e.g. `214710`)
- Full example: `reports/2026/20260315/214710.md`

```bash
mkdir -p reports/{year}/{yyyymmdd}/
```

The report must include: the user's original prompt (verbatim), executive summary, Reddit/HN/Qiita/Indie Hackers findings, per-idea concept + evidence + score table + next action, comparative summary table.

---

## Step 5: Self-Review (mandatory after every run)

1. **Script bugs** — Fix any warnings or unexpected output in the scripts.
2. **Query drift** — Add new terminology from the data to the fetch scripts' query/keyword constants.
3. **Skill gaps** — Fix ambiguous instructions in this file.
4. **Template gaps** — Fix structural issues in `references/report_template.md`.
5. **README** — Update `README.md` if structure has changed.

Report changes in Japanese at the end of the response (2–3 bullets, no separate file).

---

## Reference Files

- `references/analysis_guide.md` — How to read and cross-reference Reddit / HN / Qiita data
- `references/idea_patterns.md` — Good idea patterns and constraint adjustment guide
- `references/scoring_rubric.md` — 5-dimension scoring guide
- `references/report_template.md` — Report structure template
