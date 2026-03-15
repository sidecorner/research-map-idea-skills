# Qiita Queries — Light Information Exchange (Skill 2)

Queries used by `scripts/fetch_qiita_light_exchange.py`.

Qiita is Japan's largest developer knowledge-sharing platform (Qiita.com).
It provides strong signal on what Japanese developers are building and discussing,
complementing Reddit (English user pain points) and Hacker News (global builder/market interest).

---

## Query List (12 queries — default)

Reduced to 12 to stay within Qiita's 60 req/hour free tier in a single run.
Add `--token` to increase the limit to 1000/hour and expand queries if needed.

| Query | Type | Rationale |
|-------|------|-----------|
| `tag:匿名` | tag | Anonymous content tagged articles — implementation and design discussions |
| `tag:掲示板` | tag | Bulletin board tagged articles — architecture and moderation pain points |
| `tag:P2P` | tag | P2P sharing implementations |
| `tag:チャット 軽量` | tag | Lightweight chat — friction-reduced messaging implementations |
| `title:匿名 投稿` | title | Articles about building anonymous posting features |
| `title:匿名掲示板` | title | Anonymous bulletin board implementations |
| `title:エフェメラル` | title | Ephemeral messaging and disappearing content |
| `title:軽量 情報共有` | title | Lightweight information sharing solutions |
| `title:ハイパーローカル` | title | Hyperlocal community app discussions |
| `title:掲示板 作り` | title | "Building a bulletin board" articles — implementation pain points |
| `title:anonymous sharing` | title | English-language anonymous sharing articles by JP devs |
| `title:ephemeral` | title | English-language ephemeral content articles |

---

## Engagement Metric

Qiita uses `likes_count` (LGTM count) as the primary signal, analogous to Reddit upvotes.
`comments_count` is secondary — Qiita has less commenting culture than Reddit.

**Engagement score formula:** `likes_count + comments_count × 2`

A Qiita article with 50+ likes is strong signal; 100+ likes is viral for a technical niche.

---

## Date Range Behavior

- **Calendar year** (`--year YYYY`): filters `created_at >= YYYY-01-01` and `created_at <= YYYY-12-31`
- **Rolling window** (`--rolling`): filters past 365 days ending today — used when the target year is the current year

---

## Notes

- Qiita rate limit: 60 requests/hour (no token), 1000 requests/hour (with personal access token)
- Articles are primarily in Japanese; some developers write in English or mixed
- Qiita content reflects real implementation experience — pain points in existing tools are valuable signals
- "I tried to build X but ran into Y" articles on Qiita are particularly useful for idea validation
- Use `--token` with a Qiita personal access token to avoid rate limiting during bulk fetches
