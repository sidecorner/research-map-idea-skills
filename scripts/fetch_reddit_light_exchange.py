#!/usr/bin/env python3
"""
fetch_reddit_light_exchange.py - Fetch posts from subreddits related to
casual/lightweight information exchange for idea research.

Adapted from fetch_reddit.py for the light information exchange idea research project.

Usage:
    python scripts/fetch_reddit_light_exchange.py --year 2026 --output /tmp/reddit_light_2026.json
    python scripts/fetch_reddit_light_exchange.py --year 2025 --limit 50 --output /tmp/reddit_light_2025.json

No authentication required (uses Reddit's public JSON API).
"""

import argparse
import json
import time
import urllib.request
from datetime import datetime, timezone


# Subreddits relevant to casual/lightweight information exchange
LIGHT_EXCHANGE_SUBREDDITS = [
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
    # Hyperlocal info exchange
    "Nextdoor",
    # Lightweight social & digital minimalism
    "nosurf",
    "digitalminimalism",
    "CasualConversation",
    # Productivity / note-taking tools
    "productivity",
    "Notion",
    "ObsidianMD",
    # App discovery and indie dev
    "SideProject",
    "indiehackers",
    "AppIdeas",
    "androidapps",
    "iosapps",
    # Content discovery
    "InternetIsBeautiful",
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
    "annoying", "too complicated", "too heavy", "too much",
    "simpler", "lightweight", "quick", "easy way", "just want to",
]

# Keywords signaling lightweight information exchange topics
LIGHT_EXCHANGE_KEYWORDS = [
    "share", "sharing", "note", "tip", "quick", "casual", "simple",
    "easy", "anonymous", "ephemeral", "local", "community", "bulletin",
    "post it", "sticky note", "whiteboard", "exchange", "recommend",
    "lightweight", "minimal", "micro", "ambient", "discoverable",
    "low friction", "no account", "instant", "temporary", "disposable",
    "peer to peer", "neighbor", "nearby", "local knowledge", "ask",
    "tell", "inform", "notify", "leave a note", "pass along",
]

HEADERS = {
    "User-Agent": "LightExchangeResearch/1.0 (educational research tool)",
}


def fetch_subreddit_posts(subreddit: str, limit: int = 25, sort: str = "top",
                          target_year: int | None = None) -> list[dict]:
    """Fetch posts from a subreddit using Reddit's public JSON API."""
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


def is_light_exchange_relevant(post: dict) -> bool:
    """Heuristic: does this post relate to casual/lightweight information exchange?"""
    title = post.get("title", "").lower()
    body = post.get("selftext", "").lower()[:300]
    text = title + " " + body
    return any(kw in text for kw in LIGHT_EXCHANGE_KEYWORDS)


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
        description="Fetch light information exchange subreddit posts for idea research"
    )
    parser.add_argument("--year", type=int, default=datetime.now().year,
                        help="Target year for filtering posts (default: current year)")
    parser.add_argument("--limit", type=int, default=25,
                        help="Max posts to fetch per subreddit (default: 25)")
    parser.add_argument("--output", type=str, default="/tmp/reddit_light_raw.json",
                        help="Output JSON file path")
    parser.add_argument("--subreddits", type=str, default=None,
                        help="Comma-separated subreddit list (default: built-in list)")
    args = parser.parse_args()

    subreddits = args.subreddits.split(",") if args.subreddits else LIGHT_EXCHANGE_SUBREDDITS
    target_year = args.year

    print(f"Fetching light exchange posts from {len(subreddits)} subreddits "
          f"for year {target_year}...")

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
                "is_light_exchange_relevant": is_light_exchange_relevant(post),
            }
            all_posts.append(entry)
            if entry["is_pain_point"]:
                pain_posts.append(entry)
            if entry["is_light_exchange_relevant"]:
                relevant_posts.append(entry)

        time.sleep(1)  # be polite to Reddit's API

    # Combined list: posts that are BOTH pain points AND light-exchange relevant
    # This is the highest-signal list — use it as the primary analysis source.
    combined_posts = [p for p in all_posts if p["is_pain_point"] and p["is_light_exchange_relevant"]]

    all_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    pain_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    relevant_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
    combined_posts.sort(key=lambda x: x["engagement_score"], reverse=True)

    output = {
        "target_year": target_year,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_posts": len(all_posts),
        "pain_point_posts": len(pain_posts),
        "light_exchange_relevant_posts": len(relevant_posts),
        "combined_posts": len(combined_posts),
        "subreddits_searched": subreddits,
        "top_combined_posts": combined_posts[:50],  # pain + light-exchange — highest signal
        "top_pain_points": pain_posts[:50],
        "top_relevant_posts": relevant_posts[:50],
        "all_posts": all_posts[:100],
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Fetched {len(all_posts)} posts total.")
    print(f"  Pain point posts:         {len(pain_posts)}")
    print(f"  Light exchange relevant:  {len(relevant_posts)}")
    print(f"  Combined (pain+light):    {len(combined_posts)}")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()
