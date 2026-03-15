# Qiita Queries — Proximity Communication (Skill 1)

Queries used by `scripts/fetch_qiita_proximity.py`.

Qiita is Japan's largest developer knowledge-sharing platform (Qiita.com).
It provides strong signal on what Japanese developers are building and discussing,
complementing Reddit (English user pain points) and Hacker News (global builder/market interest).

---

## Query List (12 queries — default)

Reduced to 12 to stay within Qiita's 60 req/hour free tier in a single run.
Add `--token` to increase the limit to 1000/hour and expand queries if needed.

| Query | Type | Rationale |
|-------|------|-----------|
| `tag:BLE` | tag | BLE-tagged articles — high precision, common in iOS/Android proximity tutorials |
| `tag:Bluetooth` | tag | General Bluetooth implementation articles |
| `tag:NFC` | tag | NFC-tagged articles — tap-to-connect, contactless exchange |
| `tag:CoreBluetooth` | tag | iOS CoreBluetooth framework articles — pain points surface here |
| `tag:位置情報` | tag | Location info tagged articles |
| `tag:iBeacon` | tag | iBeacon implementations — proximity detection use cases |
| `title:すれ違い` | title | Articles mentioning StreetPass-style encounter mechanics |
| `title:BLE 近接` | title | BLE-based proximity detection implementations |
| `title:NFC 実装` | title | NFC implementation walkthroughs |
| `title:ジオフェンス` | title | Geofencing app implementations |
| `title:StreetPass` | title | StreetPass-inspired implementations |
| `title:Bluetooth proximity` | title | English-language proximity via Bluetooth articles by JP devs |

---

## Engagement Metric

Qiita uses `likes_count` (LGTM count) as the primary signal, analogous to Reddit upvotes.
`comments_count` is secondary — Qiita has less commenting culture than Reddit.

**Engagement score formula:** `likes_count + comments_count × 2`

A Qiita article with 50+ likes is strong signal; 100+ likes is viral for a technical niche.

---

## Date Range Behavior

- **Calender year** (`--year YYYY`): filters `created_at >= YYYY-01-01` and `created_at <= YYYY-12-31`
- **Rolling window** (`--rolling`): filters past 365 days ending today — used when the target year is the current year

---

## Notes

- Qiita rate limit: 60 requests/hour (no token), 1000 requests/hour (with personal access token)
- Articles are in Japanese primarily; some developers write in English or mixed
- Qiita reflects practitioner experience more than ideation — pain points in existing solutions are strong signals
- Use `--token` with a Qiita personal access token to avoid rate limiting during bulk fetches
