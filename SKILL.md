---
name: proximity-communication-idea-research
description: >
  Research and generate niche product ideas for apps or web services built around
  proximity/encounter communication (すれ違い通信) features — such as Bluetooth passive
  discovery, NFC tap-to-connect, location-based encounters, or StreetPass-style mechanics.
  Pulls real user pain points from Reddit (proximity/social/gaming subreddits) and high-engagement
  posts from Hacker News, then synthesizes actionable ideas with feasibility scoring.

  ALWAYS use this skill when the user wants to:
  - Research product ideas involving proximity communication, すれ違い通信, or encounter features
  - Discover underserved niches in location-based or Bluetooth-based social apps
  - Investigate user pain points around meeting people IRL, dating apps with proximity, or StreetPass-style UX
  - Generate scored idea candidates for a small-team or indie developer to build
---

# Proximity Communication Idea Research Skill

You are helping the user discover niche, actionable product ideas for apps or web services
centered on **proximity/encounter communication** (すれ違い通信) — the concept of passively
or actively connecting with people or content when physically nearby, without requiring
a pre-existing social relationship.

## Step 0: Confirm Target Year and Constraints (ask in Japanese)

Ask the user two questions in a single message in Japanese:

> 「以下の2点を教えてください。
>
> **① 調査対象の年号**（例：2026）
> 　指定がなければ今年（{current_year}）で進めます。
>
> **② 優先したい条件・制約**（任意）
> 　例：「iOS向け」「BLEのみ」「日本市場」「ゲーム系」「B2B SaaS」「ソロ開発」「NFC限定」「マッチング系は除く」など。
> 　なければ「なし」か空欄で構いません。」

Wait for their response. Save the values as:
- `{year}` — the target year (default: current year)
- `{constraints}` — freeform text describing the user's requirements, or empty if none

**Determining the collection date range:**

After the user responds, compute the date range for data collection:

- **If `{year}` == current year** (i.e., the year is not yet complete):
  - Use a **rolling 12-month window**: `start_date = today − 1 year`, `end_date = today`
  - Pass `--rolling` flag to all data collection scripts
  - Report this as: `**調査期間:** {start_date} 〜 {end_date}（直近1年間）`
- **If `{year}` is a past year** (fully complete):
  - Use the full calendar year: `start_date = {year}-01-01`, `end_date = {year}-12-31`
  - Pass `--year {year}` to all scripts (no `--rolling` flag)
  - Report this as: `**調査期間:** {year}-01-01 〜 {year}-12-31`

Save the computed values as `{start_date}`, `{end_date}`, and `{rolling}` (true/false).

**If constraints are provided**, note them before proceeding. They will guide idea generation and scoring in Step 3 — but do **not** narrow the data collection in Steps 1–2. Collecting broad data and then filtering ideas produces better results than filtering the data upfront.

---

## Step 1: Collect Data

Run all data collection steps from the **project root directory**
(`research-map-idea-skills/`). If you're not already there, `cd` to it first.

Use the date range flags determined in Step 0:
- Rolling window: add `--rolling` (omit `--year`)
- Past year: add `--year {year}` (omit `--rolling`)

### 1a. Reddit — Proximity Subreddits

```bash
python scripts/fetch_reddit_proximity.py \
  --year {year} \
  --limit 30 \
  --output /tmp/reddit_proximity_{year}.json
```

This fetches posts from subreddits covering proximity gaming (Pokémon GO, StreetPass),
dating/social apps (Tinder, Bumble), Bluetooth/NFC tech, privacy concerns, and indie dev.
See `references/subreddits.md` for the full list and rationale.

### 1b. Hacker News — High-Engagement Posts

**Rolling window (current year):**
```bash
python scripts/fetch_hn_proximity.py \
  --rolling \
  --min-points 10 \
  --output /tmp/hn_proximity_rolling.json
```

**Past year:**
```bash
python scripts/fetch_hn_proximity.py \
  --year {year} \
  --min-points 10 \
  --output /tmp/hn_proximity_{year}.json
```

If the result yields fewer than 10 posts, also run the previous year to supplement:

```bash
python scripts/fetch_hn_proximity.py \
  --year $((year-1)) \
  --min-points 10 \
  --output /tmp/hn_proximity_{prev_year}.json
```

See `references/hn_queries.md` for the full query list and why each one matters.

### 1c. Qiita — Japanese Developer Articles

> **Token is read automatically from `QIITA_TOKEN` environment variable.**
> If the env var is set, no `--token` flag is needed. See setup note below.

**Rolling window (current year):**
```bash
python scripts/fetch_qiita_proximity.py \
  --rolling \
  --output /tmp/qiita_proximity_rolling.json
```

**Past year:**
```bash
python scripts/fetch_qiita_proximity.py \
  --year {year} \
  --output /tmp/qiita_proximity_{year}.json
```

Qiita captures Japanese developer perspectives — implementation pain points,
architecture discussions, and "I tried to build X" articles that complement
Reddit user pain points and HN market interest.
See `references/qiita_queries_proximity.md` for the full query list.

**If the script reports `rate_limited: true`:** Partial results are still saved and usable.
Note this in the report with a caveat. It means `QIITA_TOKEN` is not set — check with
`echo $QIITA_TOKEN`.

---

## Step 2: Analyze the Data

Read all three output files. For each source:

> **If `{constraints}` were specified**, keep them in mind while reading — note which pain points and trends are especially relevant to those constraints. Don't discard other findings; you'll need the full picture to judge whether the constraints are well-served by the data.

**Reddit analysis:**
- Focus on `top_pain_points` — posts where users express frustration, unmet needs, or feature requests
- Also check `top_proximity_posts` for proximity-specific discussions
- Identify recurring themes: what do users wish existed? What is broken or missing?

**HN analysis:**
- Focus on posts with high `engagement_score` (points + 2× comments)
- High comment counts = controversy or deep interest — both are valuable signals
- Look for Show HN posts (people building something), Ask HN posts (people wanting something), and trend articles

**Qiita analysis:**
- Focus on articles with high `engagement_score` (likes + 2× comments)
- Look for "やってみた" (tried it) articles — often reveal implementation pain points
- Articles about failed approaches or unexpected limitations are especially valuable signals
- Note which tags appear on highly-liked articles — they indicate active community interest
- Qiita reflects Japanese developer practical experience; it often surfaces mobile/iOS/Android specifics that Reddit misses

**Cross-reference patterns:**
- Do Reddit users want something that HN shows builders are already trying (but failing at)?
- Does Qiita show Japanese developers encountering technical blockers that suggest an underserved niche?
- Are there pain points that appear in multiple subreddits AND on Qiita? (= strong cross-market signal)
- What categories are completely absent from all three sources (= underserved)?

---

## Step 3: Generate Ideas

Propose **3–5 product ideas** based on the research. Each idea must:

1. Have a **clear proximity/encounter communication mechanic** at its core — not just "a social app"
2. Address a **specific pain point** evidenced by the data
3. Be realistically buildable by a small team or solo developer

Good idea patterns for proximity communication:
- **Passive discovery**: "You walked past 3 people who share your interest in X" — no action required
- **Event-based encounters**: proximity features that activate during conferences, concerts, or local events
- **Context-specific communities**: hobby groups, travelers, language learners who want to meet nearby
- **Privacy-first alternatives**: opt-in encounter features that existing apps handle poorly
- **Gamified encounters**: StreetPass-style collections, stamps, or social artifacts from physical meetups
- **Wearable/physical objects**: NFC badges, QR systems, or BLE devices that enable encounters

### Applying User Constraints

If `{constraints}` were specified, apply them as follows:

- **Prioritize** ideas that naturally fit the constraints. Lead with those.
- **Adjust scoring** to reflect constraints — for example:
  - "iOS only" → lower 実現可能性 for ideas relying on BLE background scanning (OS-restricted on iOS)
  - "ソロ開発" → weight 小規模開発適性 more heavily; flag infra-heavy ideas as less suitable
  - "日本市場" → consider Japan-specific context (e.g., LINE integration potential, commuter culture, StreetPass nostalgia)
  - "B2B SaaS" → favor ideas with identifiable business buyers (event organizers, venue operators, HR tech)
- **Don't force compliance.** If the data strongly points toward an idea that conflicts with the constraints, include it as a separate "Outside constraints but high signal" section and explain why it's worth considering.
- **Note trade-offs honestly.** If a constraint makes certain ideas significantly harder (e.g., "NFC only" excludes GPS-based approaches that would score higher), say so clearly.

Score each idea using the rubric in `references/scoring_rubric.md`.

---

## Step 4: Write the Report

After analysis and idea generation, save a report following the template in `references/report_template.md`.

**File path:**
```
reports/{year}/{yyyy-mm-dd}/{HHMMSS}.md
```

Use today's actual date and current time (24-hour, no separators) for the filename.

Example: `reports/2026/2026-03-14/143022.md`

Create the directory if it doesn't exist:
```bash
mkdir -p reports/{year}/{yyyy-mm-dd}/
```

The report must include:
1. Executive summary (1–3 sentences)
   - If constraints were specified, state them at the top: `**指定条件:** {constraints}`
   - Always include: `**調査期間:** {start_date} 〜 {end_date}`
2. Reddit findings: top pain-point posts + observed themes
3. HN findings: top posts + builder/market interest themes
4. Qiita findings: top articles + Japanese developer perspectives
5. For each idea:
   - Concept description
   - How proximity communication is the core mechanic
   - Evidence from user data (specific posts/threads)
   - 5-dimension score table (see rubric)
   - Recommended next action
5. Comparative summary table with priority ranking

---

## Key Constraints

- **This skill is local to this project directory.** Do not carry findings or scripts to other projects.
- **Always use the adapted scripts** (`fetch_reddit_proximity.py` for Reddit, `fetch_hn_proximity.py` for HN, `fetch_qiita_proximity.py` for Qiita) rather than manually browsing the sites.
- **Use `--rolling` when the target year is the current year.** Never collect only a partial calendar year — always ensure a full 12 months of data.
- **Ground every idea in data.** Each proposed idea should cite at least one real Reddit post, HN thread, or Qiita article as evidence.
- **Keep ideas small-team-viable.** Don't propose ideas that require large engineering teams, regulatory approval, or hardware manufacturing at scale.
- **Respect the scoring rubric.** Don't inflate scores; honest low scores are more useful than optimistic ones.

---

## Reference Files

- `references/subreddits.md` — Subreddit list with rationale
- `references/hn_queries.md` — HN queries with design notes
- `references/qiita_queries_proximity.md` — Qiita queries with design notes
- `references/scoring_rubric.md` — Full 5-dimension scoring guide with interpretation
- `references/report_template.md` — Report structure template
- `scripts/fetch_reddit_proximity.py` — Reddit data collection script (proximity-adapted)
- `scripts/fetch_hn_proximity.py` — HN data collection script (supports `--rolling`)
- `scripts/fetch_qiita_proximity.py` — Qiita data collection script (supports `--rolling`)
