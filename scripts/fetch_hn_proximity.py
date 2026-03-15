#!/usr/bin/env python3
"""
fetch_hn_proximity.py - Fetch proximity/encounter communication posts from Hacker News
via Algolia Search API.

Adapted from fetch_hn.py for the proximity communication (すれ違い通信) idea research project.

Usage:
    python scripts/fetch_hn_proximity.py --year 2026 --output /tmp/hn_proximity_raw.json
    python scripts/fetch_hn_proximity.py --rolling --output /tmp/hn_proximity_raw.json
    python scripts/fetch_hn_proximity.py --year 2025 --min-points 5 --output /tmp/hn_proximity_raw.json

HN Algolia API is public and requires no authentication.
"""

import argparse
import json
import re
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta


# Query terms relevant to proximity/encounter communication on HN
PROXIMITY_QUERIES = [
    "proximity app",
    "location based social",
    "bluetooth proximity",
    "encounter app",
    "anonymous local",
    "nearby social network",
    "StreetPass",
    "location game",
    "serendipitous encounters",
    "hyperlocal app",
    "offline P2P",
    "NFC social",
    "mesh network social",
    "BLE beacon",
    "passive discovery",
    "geofence social",
    "find people nearby",
    "local social network",
    "proximity based",
    "digital nomad meet",
    "spontaneous social",
    "local chat app",
    "bluetooth social",
    "NFC tap",
    "random encounter app",
]

ALGOLIA_BASE = "https://hn.algolia.com/api/v1/search"

# Title-based relevance patterns (regex word-boundary to avoid false substring matches).
# e.g., r"\bble\b" won't match "customizable" or "possible".
RELEVANCE_PATTERNS = [
    r"\bble\b",                          # Bluetooth Low Energy
    r"\bnfc\b",
    r"\bbluetooth\b",
    r"\bibeacon\b",
    r"\bbeacon\b",
    r"\bgeofence[ds]?\b",
    r"\bstreetpass\b",
    r"\bproximity\b",
    r"\bhyperlocal\b",
    r"\bmesh.network\b",
    r"\bp2p\b",
    r"\bnearby\b",
    r"\bencounter\b",
    r"location[- ]based",
    r"\blocal (social|network|chat|app|community)\b",
    r"\bfind people\b",
    r"\boffline (p2p|social|mesh|chat)\b",
    r"\bserendipitous\b",
    r"\bpassive discovery\b",
    r"\bcorebluetooth\b",
]

_RELEVANCE_RE = [re.compile(p, re.IGNORECASE) for p in RELEVANCE_PATTERNS]

NOISE_PATTERNS = [
    "who is hiring", "ask hn: who is hiring",
    "freelancer? seeking freelancer", "tell hn:", "hn: announcing",
]


def is_relevant(title: str) -> bool:
    """Return True if the post title is on-topic for proximity communication."""
    title_lower = title.lower()
    if any(noise in title_lower for noise in NOISE_PATTERNS):
        return False
    return any(p.search(title) for p in _RELEVANCE_RE)


def build_timestamps(year: int, rolling: bool) -> tuple[int, int]:
    """Return (start_ts, end_ts) Unix timestamps for the target period."""
    if rolling:
        end_dt = datetime.now(timezone.utc)
        start_dt = end_dt - timedelta(days=365)
        return int(start_dt.timestamp()), int(end_dt.timestamp())
    return (
        int(datetime(year, 1, 1, tzinfo=timezone.utc).timestamp()),
        int(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc).timestamp()),
    )


def fetch_hn_posts(query: str, year: int, min_points: int = 5, rolling: bool = False) -> list[dict]:
    """Fetch HN posts matching a query within the given year or rolling 12 months."""
    year_start, year_end = build_timestamps(year, rolling)

    params = urllib.parse.urlencode({
        "query": query,
        "tags": "story",
        "numericFilters": f"created_at_i>{year_start},created_at_i<{year_end},points>={min_points}",
        "hitsPerPage": 20,
    })
    url = f"{ALGOLIA_BASE}?{params}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ProximityCommunicationResearch/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("hits", [])
    except Exception as e:
        print(f"  Warning: HN query '{query}' failed: {e}")
        return []


def normalize_post(hit: dict, query: str) -> dict:
    """Normalize an Algolia HN hit to a standard structure."""
    return {
        "object_id": hit.get("objectID", ""),
        "title": hit.get("title", ""),
        "url": hit.get("url", ""),
        "hn_url": f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
        "points": hit.get("points", 0),
        "num_comments": hit.get("num_comments", 0),
        "author": hit.get("author", ""),
        "created_at": hit.get("created_at", ""),
        "matched_query": query,
        "engagement_score": hit.get("points", 0) + hit.get("num_comments", 0) * 2,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fetch proximity communication HN posts for idea research"
    )
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target calendar year (ignored when --rolling is set; default: current year)")
    parser.add_argument("--rolling", action="store_true",
                        help="Use rolling 12-month window ending today instead of a calendar year")
    parser.add_argument("--min-points", type=int, default=5,
                        help="Minimum HN points threshold (default: 5)")
    parser.add_argument("--output", type=str, default="/tmp/hn_proximity_raw.json",
                        help="Output JSON file path")
    parser.add_argument("--queries", type=str, default=None,
                        help="Comma-separated query list (default: built-in proximity list)")
    args = parser.parse_args()

    queries = args.queries.split(",") if args.queries else PROXIMITY_QUERIES
    target_year = args.year

    if args.rolling:
        start_ts, end_ts = build_timestamps(target_year, rolling=True)
        start_d = datetime.fromtimestamp(start_ts, tz=timezone.utc).date()
        end_d = datetime.fromtimestamp(end_ts, tz=timezone.utc).date()
        period_label = f"rolling 12 months ({start_d} to {end_d})"
    else:
        period_label = f"year {target_year}"

    print(f"Fetching HN proximity posts for {period_label} using {len(queries)} queries...")

    seen_ids = set()
    all_posts = []
    filtered_count = 0

    for query in queries:
        print(f"  Searching: '{query}'...")
        hits = fetch_hn_posts(query, target_year, min_points=args.min_points, rolling=args.rolling)

        for hit in hits:
            post = normalize_post(hit, query)
            if post["object_id"] in seen_ids:
                continue
            if not is_relevant(post["title"]):
                filtered_count += 1
                continue
            seen_ids.add(post["object_id"])
            all_posts.append(post)

        time.sleep(0.5)  # gentle rate limiting

    # Sort by engagement
    all_posts.sort(key=lambda x: x["engagement_score"], reverse=True)

    start_ts, end_ts = build_timestamps(target_year, args.rolling)
    output = {
        "target_year": target_year,
        "rolling": args.rolling,
        "period": {
            "start_date": datetime.fromtimestamp(start_ts, tz=timezone.utc).date().isoformat(),
            "end_date": datetime.fromtimestamp(end_ts, tz=timezone.utc).date().isoformat(),
        },
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_posts": len(all_posts),
        "filtered_out": filtered_count,
        "queries_used": queries,
        "posts": all_posts,
        "data_note": (
            "Posts are filtered by title relevance to exclude megathreads (hiring, announcements). "
            "If result count is low, supplement with --year for the previous year."
        ),
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Found {len(all_posts)} relevant HN posts ({filtered_count} filtered out).")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()
