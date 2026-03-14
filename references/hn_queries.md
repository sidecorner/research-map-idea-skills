# Hacker News Search Queries for Proximity Communication Research

These queries are used with `scripts/fetch_hn.py` (via the Algolia HN Search API) to surface high-engagement posts relevant to proximity/encounter communication ideas.

## Primary Query List

Pass these as `--queries` to `fetch_hn.py`, or update the `PROXIMITY_QUERIES` constant if you adapt the script.

```
proximity app
location based social
bluetooth proximity
encounter app
anonymous local
nearby social network
StreetPass
location game
serendipitous encounters
local social app
proximity based
NFC social
hyperlocal app
mesh network social
offline P2P
find people nearby
location aware
geofencing social
BLE beacon
local network app
accidental meetup
random encounter app
spontaneous social
digital encounter
passive discovery
```

## Query Design Notes

### Why These Queries?

- **"proximity app"** / **"location based social"** — catch broad category discussions and Show HN posts
- **"bluetooth proximity"** / **"BLE beacon"** — surface technical implementations and feasibility posts
- **"StreetPass"** — Nintendo's iconic encounter mechanic; HN discussions often explore what made it beloved
- **"serendipitous encounters"** / **"spontaneous social"** — philosophical/product discussions about designed serendipity
- **"anonymous local"** / **"passive discovery"** — signals user desire for lower-friction encounter without full social graph exposure
- **"offline P2P"** / **"mesh network social"** — edge tech that enables encounters without internet
- **"geofencing social"** — proximity triggers, event-based encounters

### HN Signal Value

HN posts with many points (upvotes) + comments signal that a topic resonates with technical founders and early adopters — a strong proxy for:
- Technical feasibility being discussed
- Market interest from builders
- Emerging trends before mainstream coverage

## Using the Dedicated Script

Use `scripts/fetch_hn_proximity.py` which has `PROXIMITY_QUERIES` as the default:

```bash
# Default: all proximity queries, min 10 points
python scripts/fetch_hn_proximity.py --year 2026 --min-points 10 --output /tmp/hn_proximity_raw.json

# Override to specific queries only
python scripts/fetch_hn_proximity.py --year 2026 \
  --queries "proximity app,geofence social,StreetPass,BLE beacon" \
  --min-points 5 \
  --output /tmp/hn_proximity_raw.json
```

**Current-year sparsity**: If running early in the year yields fewer than 10 posts,
also run with `--year` set to the previous year to supplement with recent trends.

## Filtering Recommendations

| Parameter | Recommended Value | Rationale |
|-----------|-------------------|-----------|
| `--min-points` | 10–20 | Filter noise; focus on community-validated posts |
| `--year` | Current year | Most relevant trends; use prior years for historical context |

## Expected Output Structure

`fetch_hn.py` returns JSON with:
```json
{
  "target_year": 2026,
  "total_posts": 42,
  "queries_used": [...],
  "posts": [
    {
      "title": "Show HN: Proximity-based anonymous chat for events",
      "hn_url": "https://news.ycombinator.com/item?id=...",
      "points": 187,
      "num_comments": 63,
      "engagement_score": 437
    }
  ]
}
```

Focus on `engagement_score = points + num_comments * 2` — high comment counts indicate controversy or deep interest, both valuable signals.
