#!/usr/bin/env python3
"""
fetch_reddit.py - Fetch posts from subreddits relevant to proximity/encounter
communication and lightweight information exchange for idea research.

Usage:
    python scripts/fetch_reddit.py --year 2026 --output /tmp/reddit_raw.json
    python scripts/fetch_reddit.py --year 2025 --limit 50 --output /tmp/reddit_2025.json

No authentication required (uses Reddit's public JSON API).
"""

import argparse
import json
import time
import urllib.request
from datetime import datetime, timezone


# Subreddits covering proximity communication, lightweight info exchange,
# and adjacent communities (indie dev, privacy, hyperlocal, casual social).
SUBREDDITS = [
    # Location-based gaming & StreetPass mechanics
    "pokemongo",
    "Ingress",
    "NianticWayfarer",
    "streetpass",
    # Tech: Bluetooth, NFC, local networking
    "bluetooth",
    "NFC",
    "IoT",
    "embedded",
    # Hyperlocal & community apps
    "Nextdoor",
    "digitalnomad",
    # Privacy / concerns around proximity tracking
    "privacy",
    "privacytoolsIO",
    # Wearables & hardware
    "wearables",
    "smartwatch",
    # Casual Q&A and knowledge sharing
    "AskReddit",
    "NoStupidQuestions",
    "tipofmytongue",
    "explainlikeimfive",
    # Lightweight idea/thought sharing
    "Showerthoughts",
    "mildlyinteresting",
    "lifehacks",
    # Anonymous / low-barrier expression
    "confession",
    "offmychest",
    "TrueOffMyChest",
    # Lightweight social & digital minimalism
    "nosurf",
    "digitalminimalism",
    "CasualConversation",
    # Productivity / note-taking tools
    "productivity",
    "Notion",
    "ObsidianMD",
    # App dev / startup angle
    "startups",
    "Entrepreneur",
    "SideProject",
    "indiehackers",
    "AppIdeas",
    "androidapps",
    "iosapps",
    # Community Q&A format reference
    "personalfinance",
    "legaladvice",
]

# Keywords that signal user pain points or unmet needs
PAIN_SIGNAL_KEYWORDS = [
    "help", "advice", "question", "rant", "frustrated", "can't find",
    "looking for", "recommendation", "issue", "problem", "struggle",
    "disappointed", "wish", "need", "overwhelmed", "confused",
    "why doesn't", "feature request", "missing", "lack", "no way to",
    "wish there was", "alternative", "better than", "replace",
    "annoying", "broken", "privacy concern", "creepy", "stalker",
    "too complicated", "too heavy", "too much",
    "simpler", "lightweight", "quick", "easy way", "just want to",
]

# Keywords signaling proximity/encounter communication or lightweight info exchange.
# IMPORTANT: All entries must be specific compound phrases or rare domain terms.
# Avoid short common words ("tip", "meet", "local", "share") — they substring-match
# unrelated posts (e.g., "irl" matches "girl", "tip" matches "tipped off").
RELEVANCE_KEYWORDS = [
    # Proximity / encounter — specific tech/concept terms
    "proximity", "bluetooth", "nfc", " ble ", "streetpass",
    "pass by", "serendipitous", "mesh network",
    "peer to peer", " p2p ", "hyperlocal", "geofence",
    "location based", "location-based", "find people near",
    "nearby people", "nearby users", "nearby stranger",
    "encounter app", "encounter feature",
    # Lightweight info exchange — specific compound phrases only
    "anonymous note", "anonymous post", "anonymous app", "anonymous chat",
    "anonymous sharing", "anonymous message",
    "ephemeral", "leave a note", "leave a message",
    "local bulletin", "bulletin board app",
    "no account", "no login required", "no sign",
    "low friction", "neighborhood app", "local tips app",
    "local knowledge sharing", "disposable social",
    "hyperlocal app", "ambient social",
]

HEADERS = {
    "User-Agent": "ProximityLightExchangeResearch/1.0 (educational research tool)",
}


def fetch_subreddit_posts(subreddit: str, limit: int = 25, sort: str = "top",
                          target_year: int | None = None) -> list[dict]:
    """Fetch posts from a subreddit using Reddit's public JSON API.

    When target_year is the current year or next year, uses t=year (past 12 months).
    For past years, uses t=all and applies client-side year filtering — note that
    Reddit's public API only returns up to ~1000 top posts, so coverage of older
    years may be incomplete.
    """
    current_year = datetime.now(timezone.utc).year
    time_filter = "year" if target_year is None or target_year >= current_year - 1 else "all"
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}&t={time_filter}"
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            posts = data.get("data", {}).get("children", [])
            return [p["data"] for p in posts]
    except Exception as e:
        print(f"  Warning: Failed to fetch r/{subreddit}: {e}")
        return []


def is_pain_point(post: dict) -> bool:
    """Heuristic: does this post signal a user pain point?"""
    title = post.get("title", "").lower()
    flair = (post.get("link_flair_text") or "").lower()
    body = post.get("selftext", "").lower()[:300]
    text = title + " " + flair + " " + body
    return any(kw in text for kw in PAIN_SIGNAL_KEYWORDS)


def is_relevant(post: dict) -> bool:
    """Heuristic: does this post relate to proximity communication or lightweight info exchange?"""
    title = post.get("title", "").lower()
    body = post.get("selftext", "").lower()[:300]
    text = title + " " + body
    return any(kw in text for kw in RELEVANCE_KEYWORDS)


def filter_by_year(post: dict, year: int) -> bool:
    """Filter posts created in the given year."""
    created = post.get("created_utc", 0)
    post_year = datetime.fromtimestamp(created, tz=timezone.utc).year
    return post_year == year


def score_post(post: dict) -> int:
    """Simple engagement score combining upvotes and comment count."""
    return post.get("score", 0) + post.get("num_comments", 0) * 3


def main():
    parser = argparse.ArgumentParser(
        description="Fetch subreddit posts for proximity/light-exchange idea research"
    )
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target year for filtering posts (default: current year)")
    parser.add_argument("--limit", type=int, default=25,
                        help="Max posts to fetch per subreddit (default: 25)")
    parser.add_argument("--output", type=str, default="/tmp/reddit_raw.json",
                        help="Output JSON file path")
    parser.add_argument("--subreddits", type=str, default=None,
                        help="Comma-separated subreddit list (default: built-in list)")
    args = parser.parse_args()

    subreddits = args.subreddits.split(",") if args.subreddits else SUBREDDITS
    target_year = args.year

    print(f"Fetching posts from {len(subreddits)} subreddits for year {target_year}...")

    all_posts = []
    pain_posts = []
    relevant_posts = []

    current_year = datetime.now(timezone.utc).year
    # When target_year is current (or recent), Reddit uses t=year (rolling 12 months).
    # Client-side year filter would discard valid older posts — skip it in rolling mode.
    use_strict_year_filter = target_year < current_year - 1

    for sub in subreddits:
        print(f"  Fetching r/{sub}...")
        posts = fetch_subreddit_posts(sub, limit=args.limit, sort="top", target_year=target_year)

        for post in posts:
            # Apply strict year filter only for past years fetched with t=all
            if use_strict_year_filter and not filter_by_year(post, target_year):
                continue

            entry = {
                "subreddit": sub,
                "title": post.get("title", ""),
                "selftext": post.get("selftext", "")[:500],
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "flair": post.get("link_flair_text", ""),
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "created_utc": post.get("created_utc", 0),
                "engagement_score": score_post(post),
                "is_pain_point": is_pain_point(post),
                "is_relevant": is_relevant(post),
            }
            all_posts.append(entry)
            if entry["is_pain_point"]:
                pain_posts.append(entry)
            if entry["is_relevant"]:
                relevant_posts.append(entry)

        time.sleep(1)  # be polite to Reddit's API

    # Combined list: posts that are BOTH pain points AND relevant
    # This is the highest-signal list — use it as the primary analysis source.
    combined_posts = [p for p in all_posts if p["is_pain_point"] and p["is_relevant"]]

    # Sort by engagement
    all_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    pain_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    relevant_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    combined_posts.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "target_year": target_year,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_posts": len(all_posts),
        "pain_point_posts": len(pain_posts),
        "relevant_posts": len(relevant_posts),
        "combined_posts": len(combined_posts),
        "subreddits_searched": subreddits,
        "top_combined_posts": combined_posts[:50],   # pain + relevant — highest signal
        "top_pain_points": pain_posts[:50],
        "top_relevant_posts": relevant_posts[:50],
        "all_posts": all_posts[:100],
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Fetched {len(all_posts)} posts total.")
    print(f"  Pain point posts:  {len(pain_posts)}")
    print(f"  Relevant posts:    {len(relevant_posts)}")
    print(f"  Combined:          {len(combined_posts)}")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()
