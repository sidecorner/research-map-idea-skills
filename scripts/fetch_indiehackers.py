#!/usr/bin/env python3
"""
fetch_indiehackers.py - Fetch posts from Indie Hackers via Firebase REST API.

Usage:
    python scripts/fetch_indiehackers.py --rolling --output /tmp/ih_rolling.json
    python scripts/fetch_indiehackers.py --year 2025 --output /tmp/ih_2025.json
    python scripts/fetch_indiehackers.py --rolling --limit 100 --output /tmp/ih_rolling.json

Data source:
    Firebase Realtime Database (public, no auth required)
    https://indie-hackers.firebaseio.com/posts.json

Fields available:
    title, body, groupName, numReplies, numViews, numLinkClicks, createdTimestamp, username

No authentication required.
"""

import argparse
import json
import re
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta


FIREBASE_BASE = "https://indie-hackers.firebaseio.com/posts.json"

# Keywords for relevance filtering — same themes as HN / Reddit scripts.
# Must appear in title or body to be included.
RELEVANCE_PATTERNS = [
    # Proximity / encounter / location
    r"\bble\b",
    r"\bbluetooth\b",
    r"\bgeofence[ds]?\b",
    r"\bstreetpass\b",
    r"\bproximity\b",
    r"\bhyperlocal\b",
    r"\bp2p\b",
    r"\bnearby\b",
    r"location[- ]based",
    r"\bgps\b",
    r"\bgeolocation\b",
    r"location.unlock",
    r"check.?in",
    # Lightweight / casual info exchange
    r"\bephemeral\b",
    r"\banonymous\b",
    r"bulletin.?board",
    r"local.?chat",
    r"local.?social",
    r"community.?board",
    r"neighborhood.?app",
    r"hyperlocal",
    r"local.?tips",
    r"local.?knowledge",
    r"local.?q.?&.?a",
    r"no.?account",
    r"no.?login",
    r"map.?based",
    r"mapbox",
    r"google.?maps",
    r"geo.?lock",
    r"geo.?fence",
    r"local.?network",
    r"local.?market",
    # Indie dev / small team context
    r"solo.?founder",
    r"indie.?hacker",
    r"side.?project",
    r"small.?team",
    r"micro.?saas",
    r"niche.?app",
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in RELEVANCE_PATTERNS]

BATCH_SIZE = 300  # Firebase limit per request


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch Indie Hackers posts via Firebase REST API")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--rolling", action="store_true",
                       help="Fetch rolling 12 months from today")
    group.add_argument("--year", type=int,
                       help="Fetch full calendar year (e.g. 2025)")
    parser.add_argument("--limit", type=int, default=500,
                        help="Max posts to fetch before keyword filtering (default: 500)")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--min-replies", type=int, default=0,
                        help="Minimum numReplies to include (default: 0)")
    return parser.parse_args()


def date_range(args):
    now = datetime.now(timezone.utc)
    if args.rolling:
        start = now - timedelta(days=365)
        end = now
        label = f"rolling 12 months ({start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')})"
    else:
        start = datetime(args.year, 1, 1, tzinfo=timezone.utc)
        end = datetime(args.year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        label = f"{args.year} full year"
    return start, end, label


def to_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def fetch_batch(start_ms: int, end_ms: int, limit: int) -> dict:
    params = urllib.parse.urlencode({
        "orderBy": '"createdTimestamp"',
        "startAt": start_ms,
        "endAt": end_ms,
        "limitToFirst": min(limit, BATCH_SIZE),
    })
    url = f"{FIREBASE_BASE}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"  [WARNING] Firebase fetch error: {e}")
        return {}


def is_relevant(post: dict) -> bool:
    text = f"{post.get('title', '')} {post.get('body', '')}"
    return any(p.search(text) for p in COMPILED_PATTERNS)


def engagement_score(post: dict) -> float:
    """
    Weighted engagement: replies × 10 + link_clicks × 3 + views × 0.01
    Replies signal discussion quality. Views alone can be noise (job posts).
    """
    return (
        post.get("numReplies", 0) * 10
        + post.get("numLinkClicks", 0) * 3
        + post.get("numViews", 0) * 0.01
    )


def main():
    args = parse_args()
    start_dt, end_dt, label = date_range(args)
    start_ms = to_ms(start_dt)
    end_ms = to_ms(end_dt)

    print(f"Fetching Indie Hackers posts for {label}")
    print(f"  Limit: {args.limit} | Min replies: {args.min_replies} | Filter: ON")

    all_posts = {}
    fetched = 0
    cursor_ms = start_ms

    while fetched < args.limit:
        remaining = args.limit - fetched
        batch = fetch_batch(cursor_ms, end_ms, remaining)
        if not batch:
            break

        new_posts = {k: v for k, v in batch.items() if k not in all_posts}
        all_posts.update(new_posts)
        fetched += len(batch)

        # Advance cursor past the last seen timestamp to paginate
        last_ts = max((v.get("createdTimestamp", 0) for v in batch.values()), default=0)
        if last_ts <= cursor_ms or len(batch) < BATCH_SIZE:
            break  # No more data or last page
        cursor_ms = last_ts + 1

        time.sleep(0.5)

    print(f"  Fetched {len(all_posts)} raw posts total")

    # Filter by min_replies
    if args.min_replies > 0:
        all_posts = {k: v for k, v in all_posts.items()
                     if v.get("numReplies", 0) >= args.min_replies}

    # Filter by relevance keywords
    relevant = {k: v for k, v in all_posts.items() if is_relevant(v)}
    filtered_out = len(all_posts) - len(relevant)
    print(f"  Relevant posts: {len(relevant)} ({filtered_out} filtered out as off-topic)")

    # Build output records
    records = []
    for key, post in relevant.items():
        ts = post.get("createdTimestamp", 0)
        created_at = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d") if ts else ""
        score = engagement_score(post)
        records.append({
            "id": key,
            "title": post.get("title", "").strip(),
            "body_snippet": post.get("body", "")[:300].strip(),
            "group": post.get("groupName", ""),
            "username": post.get("username", ""),
            "num_replies": post.get("numReplies", 0),
            "num_views": post.get("numViews", 0),
            "num_link_clicks": post.get("numLinkClicks", 0),
            "engagement_score": round(score, 1),
            "created_at": created_at,
            "url": f"https://www.indiehackers.com/post/{key}",
        })

    records.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "period": label,
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_raw": len(all_posts),
        "total_relevant": len(records),
        "filtered_out": filtered_out,
        "posts": records,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Done! Found {len(records)} relevant posts.")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()
