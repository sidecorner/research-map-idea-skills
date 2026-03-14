---
name: light-information-exchange-idea-research
description: >
  Research and generate niche product ideas for apps or web services centered on
  casual, lightweight information exchange — such as ephemeral local notes, anonymous
  peer Q&A, low-friction tip sharing, ambient community boards, or "leave a message here"
  mechanics. Pulls real user pain points from Reddit (casual Q&A, anonymous sharing,
  digital minimalism, indie dev subreddits) and high-engagement Hacker News posts, then
  synthesizes actionable ideas with feasibility scoring.

  ALWAYS use this skill when the user wants to:
  - Research product ideas for lightweight, casual, or low-friction information sharing
  - Explore anonymous sharing, ephemeral notes, hyperlocal bulletin boards, or micro-social concepts
  - Find alternatives to heavy social media for simple, quick information exchange
  - Investigate user pain points around note sharing, peer Q&A, community tips, or ambient social UX
  - Generate scored idea candidates for a small-team or indie developer to build in the info-sharing space
---

# Light Information Exchange Idea Research Skill

You are helping the user discover niche, actionable product ideas for apps or web services
centered on **casual, lightweight information exchange** — the concept of sharing useful,
contextual, or ephemeral information with others in a low-friction, low-identity, or
low-commitment way. Think anonymous local notes, peer tips, community bulletin boards,
"leave a message here" mechanics, or ambient knowledge discovery — as opposed to
full social networking or messaging platforms.

## Step 0: Confirm Target Year and Constraints (ask in Japanese)

Ask the user two questions in a single message in Japanese:

> 「以下の2点を教えてください。
>
> **① 調査対象の年号**（例：2026）
> 　指定がなければ今年（{current_year}）で進めます。
>
> **② 優先したい条件・制約**（任意）
> 　例：「匿名性重視」「位置情報なし」「Web のみ」「日本市場」「B2B 向け」「ソロ開発」「ゲーミフィケーションあり」「モデレーション不要」など。
> 　なければ「なし」か空欄で構いません。」

Wait for their response. Save:
- `{year}` — target year (default: current year)
- `{constraints}` — freeform constraints text, or empty

**If constraints are provided**, note them before proceeding. They guide idea generation
in Step 3, but do **not** narrow the data collection in Steps 1–2. Broad data collection
followed by constrained filtering produces sharper, more defensible ideas.

---

## Step 1: Collect Data

Run both scripts from the **project root directory** (`research-map-idea-skills/`).

### 1a. Reddit — Light Exchange Subreddits

```bash
python scripts/fetch_reddit_light_exchange.py \
  --year {year} \
  --limit 30 \
  --output /tmp/reddit_light_{year}.json
```

This fetches from subreddits covering casual Q&A, anonymous expression, digital minimalism,
productivity tools, and indie dev. See `references/light_exchange_subreddits.md` for the
full list and rationale.

### 1b. Hacker News — High-Engagement Posts

```bash
python scripts/fetch_hn_light_exchange.py \
  --year {year} \
  --min-points 5 \
  --output /tmp/hn_light_{year}.json
```

If the current year yields fewer than 10 posts, also supplement with the previous year:

```bash
python scripts/fetch_hn_light_exchange.py \
  --year $((year-1)) \
  --min-points 5 \
  --output /tmp/hn_light_{prev_year}.json
```

See `references/light_exchange_hn_queries.md` for query design notes.

---

## Step 2: Analyze the Data

Read both output files. For each source:

> **If `{constraints}` were specified**, keep them in mind while reading — note which pain
> points and trends are especially relevant. Don't discard other findings; you'll need the
> full picture to evaluate whether the constraints are well-served.

**Reddit analysis:**
- Focus on `top_pain_points` — posts where users express frustration, unmet needs, or tool gaps
- Also check `top_relevant_posts` for lightweight sharing use cases
- Look for: "I just want a simple way to…", "why is there no app that…", "I use X for this but it's too heavy"
- Note which subreddits have the most signal — different communities have different friction points

**HN analysis:**
- Focus on posts with high `engagement_score` (points + 2× comments)
- Watch for Show HN posts (builders trying this), post-mortems (what failed and why),
  and Ask HN threads (explicit demand statements)
- High comment counts with controversial tone often reveal structural tensions — e.g., "anonymous = abuse"

**Cross-reference patterns:**
- Where does Reddit demand something that HN builders have tried but abandoned?
- What friction points appear across multiple communities? (e.g., "too many steps", "requires account")
- What existing platforms are being repurposed for lightweight exchange? (e.g., using Notion as a bulletin board, using Reddit for Q&A because nothing lighter exists)
- What categories are completely absent from HN builds? (= no one has tried it yet)

---

## Step 3: Generate Ideas

Propose **3–5 product ideas** based on the research. Each idea must:

1. Have **lightweight information exchange** as its core mechanic — not full messaging, not heavy social
2. Solve a **specific friction point** evidenced by the data
3. Be realistically buildable by a small team or solo developer

Good idea patterns for lightweight information exchange:

- **Ephemeral community boards**: Notes, tips, or questions that expire — no permanent record, no follower counts
- **Context-triggered sharing**: Leave a note tied to a place, event, or object that others discover passively
- **Anonymous peer Q&A**: Ask anything without an account; community answers without identity pressure
- **Micro-knowledge exchange**: Single tips, micro-recommendations, or one-liner observations — no long posts
- **Pull-only discovery**: Information you go looking for, not pushed at you — low cognitive load
- **Trust-layered anonymity**: Progressively reveal identity as trust builds — reduces abuse while preserving entry-point friction-free
- **Artifact-based exchange**: Physical or digital objects (QR stickers, NFC tags, shared documents) as the carrier of the exchange

### Applying User Constraints

If `{constraints}` were specified:

- **Prioritize** ideas that naturally fit the constraints. Lead with those.
- **Adjust scoring** to reflect constraints — for example:
  - "匿名性重視" → favor ephemeral/no-account designs; flag identity-linked approaches as misaligned
  - "位置情報なし" → avoid geofence or GPS-dependent mechanics; favor interest/context-based discovery
  - "モデレーション不要" → prefer designs with structural abuse prevention (expiry, rate limiting, vote-down) over human moderation
  - "B2B 向け" → favor team/org-internal bulletin boards, knowledge bases with light UX, or event organizer tools
  - "ソロ開発" → weight 小規模開発適性 heavily; deprioritize real-time or moderation-heavy ideas
- **Don't force compliance.** If data strongly points to a high-potential idea outside the constraints, include it as a separate "制約外だが注目" section with an explanation.
- **Note trade-offs honestly.** If a constraint eliminates a whole class of ideas, say so.

Score each idea using the rubric in `references/scoring_rubric.md`.

---

## Step 4: Write the Report

Save a report following the template in `references/report_template.md`.

**File path:**
```
reports/{year}/{yyyy-mm-dd}/{HHMMSS}.md
```

```bash
mkdir -p reports/{year}/{yyyy-mm-dd}/
```

The report must include:
1. Executive summary (1–3 sentences)
   - If constraints were specified: `**指定条件:** {constraints}`
   - Tag the report topic: `**調査テーマ:** ライトな情報交換`
2. Reddit findings: top pain-point posts + observed themes
3. HN findings: top posts + builder/market interest themes
4. For each idea:
   - Concept description
   - What makes the exchange feel "light" — specifically how friction is reduced
   - Evidence from user data (specific posts/threads)
   - 5-dimension score table (see rubric)
   - Recommended next action
5. Comparative summary table with priority ranking

---

## Key Constraints

- **This skill is local to this project directory.** Do not carry findings or scripts to other projects.
- **Always use the dedicated scripts** (`fetch_reddit_light_exchange.py`, `fetch_hn_light_exchange.py`) rather than manually browsing.
- **Ground every idea in data.** Each proposed idea should cite at least one real Reddit post or HN thread.
- **Keep ideas small-team-viable.** Don't propose ideas requiring large moderation teams, complex ML pipelines, or regulatory approval.
- **Lightness is a design constraint, not just a metaphor.** For each idea, be explicit about what has been removed or simplified compared to a full social platform.
- **Respect the scoring rubric.** Don't inflate scores; honest low scores are more useful than optimistic ones.

---

## Reference Files

- `references/light_exchange_subreddits.md` — Subreddit list with rationale
- `references/light_exchange_hn_queries.md` — HN queries with design notes
- `references/scoring_rubric.md` — Full 5-dimension scoring guide (shared with proximity skill)
- `references/report_template.md` — Report structure template (shared with proximity skill)
- `scripts/fetch_reddit_light_exchange.py` — Reddit data collection script
- `scripts/fetch_hn_light_exchange.py` — HN data collection script
