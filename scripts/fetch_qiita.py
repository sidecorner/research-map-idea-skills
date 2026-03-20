#!/usr/bin/env python3
"""
fetch_qiita.py - Fetch proximity/encounter communication and lightweight information
exchange articles from Qiita via Qiita API v2.

Usage:
    python scripts/fetch_qiita.py --rolling --output /tmp/qiita_rolling.json
    python scripts/fetch_qiita.py --rolling --token YOUR_TOKEN --output /tmp/qiita_rolling.json
    python scripts/fetch_qiita.py --year 2025 --output /tmp/qiita_2025.json

Rate limits:
    - No token:  60 requests/hour  → 24 queries at 2s sleep fits comfortably
    - With token: 1000 requests/hour → no concern

Query strategy:
    - Uses "tag:X" and "title:X" forms for precision over full-text search
    - Post-filtering ensures only relevant articles are kept

Obtaining a Qiita token (free):
    https://qiita.com/settings/applications → Personal Access Token → read_qiita scope
"""

import argparse
import json
import os
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta


# Queries covering both proximity communication and lightweight info exchange.
# 24 total — fits within the 60 req/hr free tier (24 requests at 2s sleep ≈ 48 seconds).
QUERIES = [
    # Proximity / encounter communication
    "tag:BLE",
    "tag:Bluetooth",
    "tag:CoreBluetooth",
    "tag:位置情報",
    "tag:iBeacon",
    "title:すれ違い",
    "title:BLE 近接",
    "title:ジオフェンス",
    "title:StreetPass",
    "title:Bluetooth proximity",
    "title:GPS 位置情報",
    # Lightweight information exchange
    "tag:匿名",
    "tag:掲示板",
    "tag:P2P",
    "tag:チャット 軽量",
    "title:匿名 投稿",
    "title:匿名掲示板",
    "title:エフェメラル",
    "title:軽量 情報共有",
    "title:ハイパーローカル",
    "title:掲示板 作り",
    "title:anonymous sharing",
    "title:ephemeral",
]

# Keywords for post-filtering: article title OR any tag must contain at least one.
RELEVANCE_KEYWORDS = [
    # Proximity / encounter (Japanese + English)
    "ble", "bluetooth", "近接", "すれ違い", "streetpass", "ビーコン",
    "位置情報", "gps", "ジオフェンス", "ibeacon", "geofence", "mesh",
    "proximity", "corebluetooth", "p2p", "offline", "encounter", "location",
    "nearby", "beacon",
    # Lightweight info exchange (Japanese + English)
    # NOTE: avoid generic Japanese terms like 軽量 (matches lightweight framework articles),
    # チャット (matches any chat implementation), メモ (matches any note-taking tool),
    # 投稿 (matches any blog post), コミュニティ (matches any community article)
    "匿名", "掲示板", "エフェメラル", "使い捨て", "ハイパーローカル",
    "匿名投稿", "匿名共有", "匿名掲示板", "位置情報共有",
    "anonymous", "ephemeral", "bulletin board", "hyperlocal",
    "low friction", "disposable social", "ambient social",
]

QIITA_BASE = "https://qiita.com/api/v2/items"
MAX_CONSECUTIVE_403 = 3  # Stop early if rate limited persistently


def build_date_range(year: int, rolling: bool) -> tuple[str, str]:
    """Compute (start_date, end_date) strings in YYYY-MM-DD format."""
    if rolling:
        end_dt = datetime.now(timezone.utc)
        start_dt = end_dt - timedelta(days=365)
        return start_dt.date().isoformat(), end_dt.date().isoformat()
    return f"{year}-01-01", f"{year}-12-31"


def is_relevant(item: dict) -> bool:
    """Return True if the article title or tags match a relevance keyword."""
    title_lower = item.get("title", "").lower()
    tags_lower = " ".join(t["name"] for t in item.get("tags", [])).lower()
    combined = title_lower + " " + tags_lower
    return any(kw in combined for kw in RELEVANCE_KEYWORDS)


def fetch_qiita_items(
    query: str,
    start_date: str,
    end_date: str,
    token: str | None = None,
    per_page: int = 20,
) -> list[dict] | None:
    """
    Fetch Qiita items for a query within the date range.
    Returns None on rate-limit (403); returns [] on other errors.
    """
    full_query = f"{query} created:>={start_date} created:<={end_date}"
    params = urllib.parse.urlencode({
        "query": full_query,
        "page": 1,
        "per_page": per_page,
    })
    url = f"{QIITA_BASE}?{params}"

    headers = {"User-Agent": "ProximityLightExchangeResearch/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            items = json.loads(response.read().decode("utf-8"))
            return items if isinstance(items, list) else []
    except Exception as e:
        if "403" in str(e):
            return None  # Signal rate limit to caller
        print(f"  Warning: Qiita query '{query}' failed: {e}")
        return []


def normalize_item(item: dict, query: str) -> dict:
    """Normalize a Qiita API item to a standard structure."""
    likes = item.get("likes_count", 0)
    comments = item.get("comments_count", 0)
    return {
        "id": item.get("id", ""),
        "title": item.get("title", ""),
        "url": item.get("url", ""),
        "likes_count": likes,
        "comments_count": comments,
        "tags": [t["name"] for t in item.get("tags", [])],
        "author": item.get("user", {}).get("id", ""),
        "created_at": item.get("created_at", ""),
        "matched_query": query,
        "engagement_score": likes + comments * 2,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fetch proximity/light-exchange Qiita articles for idea research"
    )
    parser.add_argument(
        "--year", type=int, default=datetime.now().year,
        help="Target calendar year (ignored when --rolling is set; default: current year)"
    )
    parser.add_argument(
        "--rolling", action="store_true",
        help="Use rolling 12-month window ending today instead of a calendar year"
    )
    parser.add_argument(
        "--min-likes", type=int, default=3,
        help="Minimum likes threshold to keep an article (default: 3)"
    )
    parser.add_argument(
        "--output", type=str, default="/tmp/qiita_raw.json",
        help="Output JSON file path"
    )
    parser.add_argument(
        "--token", type=str, default=None,
        help=(
            "Qiita personal access token (overrides QIITA_TOKEN env var). "
            "Increases rate limit from 60 to 1000 req/hour. "
            "Set once with: export QIITA_TOKEN=your_token in ~/.zshrc"
        )
    )
    parser.add_argument(
        "--queries", type=str, default=None,
        help="Comma-separated query list (default: built-in list)"
    )
    parser.add_argument(
        "--no-filter", action="store_true",
        help="Disable relevance post-filtering (include all results)"
    )
    args = parser.parse_args()

    queries = args.queries.split(",") if args.queries else QUERIES
    start_date, end_date = build_date_range(args.year, args.rolling)

    # Resolve token: --token > QIITA_TOKEN env var > ~/.config/qiita/token > .env
    token = args.token or os.environ.get("QIITA_TOKEN")
    if not token:
        token_file = os.path.expanduser("~/.config/qiita/token")
        if os.path.exists(token_file):
            token = open(token_file).read().strip() or None
    if not token:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        if os.path.exists(env_file):
            for line in open(env_file).read().splitlines():
                if line.startswith("QIITA_TOKEN="):
                    token = line.split("=", 1)[1].strip() or None
                    break

    period_label = (
        f"rolling 12 months ({start_date} to {end_date})"
        if args.rolling else f"year {args.year}"
    )
    print(f"Fetching Qiita articles for {period_label}")
    print(f"  Queries: {len(queries)} | Min likes: {args.min_likes} | "
          f"Filter: {'OFF' if args.no_filter else 'ON'}")

    if not token:
        print("  ⚠ No token. Rate limit: 60 req/hour.")
        print("    Fix: add QIITA_TOKEN=xxx to .env in project root")
    elif args.token:
        print("  ✓ Token: --token flag. Rate limit: 1000 req/hour.")
    elif os.environ.get("QIITA_TOKEN"):
        print("  ✓ Token: QIITA_TOKEN env var. Rate limit: 1000 req/hour.")
    else:
        print("  ✓ Token: config/dotenv file. Rate limit: 1000 req/hour.")

    # Sleep: conservative without token, fast with token
    sleep_sec = 2.0 if not token else 0.5

    seen_ids: set[str] = set()
    all_items: list[dict] = []
    filtered_count = 0
    consecutive_403 = 0
    rate_limited = False

    for query in queries:
        print(f"  Searching: '{query}'...")
        result = fetch_qiita_items(query, start_date, end_date, token=token)

        if result is None:
            consecutive_403 += 1
            print(f"  ⚠ Rate limited (403). [{consecutive_403}/{MAX_CONSECUTIVE_403}]")
            if consecutive_403 >= MAX_CONSECUTIVE_403:
                print(f"  Stopping early after {MAX_CONSECUTIVE_403} consecutive 403s.")
                print("  Use --token to avoid this. Saving collected results so far.")
                rate_limited = True
                break
            time.sleep(5)  # Brief pause before next attempt
            continue

        consecutive_403 = 0  # Reset on success
        for item in result:
            normalized = normalize_item(item, query)
            if normalized["id"] in seen_ids:
                continue
            if normalized["likes_count"] < args.min_likes:
                continue
            if not args.no_filter and not is_relevant(item):
                filtered_count += 1
                continue
            seen_ids.add(normalized["id"])
            all_items.append(normalized)

        time.sleep(sleep_sec)

    all_items.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "period": {"start_date": start_date, "end_date": end_date, "rolling": args.rolling},
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_items": len(all_items),
        "filtered_out": filtered_count,
        "rate_limited": rate_limited,
        "queries_used": queries,
        "items": all_items,
        "data_note": (
            "Qiita reflects Japanese developer community perspectives. "
            "Queries use tag:/title: forms for precision. "
            "Results are post-filtered to ensure relevance. "
            "Rate limit: 60 req/hour (no token) / 1000 req/hour (with token)."
        ),
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    status = " ⚠ (rate limited — partial results)" if rate_limited else ""
    print(f"\nDone{status}! Found {len(all_items)} relevant Qiita articles "
          f"({filtered_count} filtered out as off-topic).")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()
