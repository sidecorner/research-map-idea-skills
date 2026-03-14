# Hacker News Search Queries for Light Information Exchange Research

These queries are used with `scripts/fetch_hn_light_exchange.py` to surface high-engagement
posts relevant to casual/lightweight information exchange app ideas.

## Primary Query List

```
ephemeral messaging
anonymous sharing app
local knowledge sharing
casual social app
micro social network
lightweight social
local bulletin board
anonymous notes app
quick note sharing
community Q&A app
local tips app
peer recommendations
ambient social
low friction sharing
digital post-it
information exchange app
hyperlocal sharing
disposable social
no account sharing
instant anonymous
leave a message
neighborhood app
micro blogging
casual information
serendipitous discovery
```

## Query Design Notes

### Why These Queries?

- **"ephemeral messaging"** / **"disposable social"** — surfaces the demand for and failures of Snapchat-era anonymity; discussions often include what comes next
- **"anonymous sharing app"** / **"instant anonymous"** — catches technical and ethical debates around identity-free sharing, including YikYak post-mortems
- **"local bulletin board"** / **"neighborhood app"** / **"hyperlocal sharing"** — the digital equivalent of community notice boards; under-explored in mobile
- **"low friction sharing"** / **"no account sharing"** — captures the frustration with high-barrier tools; Show HN posts that deliberately remove signup
- **"ambient social"** / **"serendipitous discovery"** — philosophical/product discussions about passive, non-demanding information presence
- **"micro social network"** / **"lightweight social"** — HN builders who are explicitly trying to counter heavy social platforms
- **"community Q&A app"** / **"peer recommendations"** — the successor-to-Reddit space; what's next in structured peer knowledge exchange
- **"digital post-it"** / **"leave a message"** — physical metaphors for lightweight ephemeral notes, often location-tied

### HN Signal Patterns to Watch

| Pattern | What It Signals |
|---------|----------------|
| High comments, low points | Controversial or polarizing feature — people have strong opinions |
| Show HN with many comments | Builders are exploring the space; community has feedback |
| Ask HN with many responses | Unmet need explicitly named by community |
| Post-mortem or "lessons learned" | Someone tried and failed — reveals structural obstacles |

## Filtering Recommendations

| Parameter | Recommended Value | Rationale |
|-----------|-------------------|-----------|
| `--min-points` | 5–10 | Lower threshold than proximity — this space has fewer niche posts, so catch more |
| `--year` | Current year | Trends move fast in social apps; supplement with previous year if sparse |

## Expected Output Structure

`fetch_hn_light_exchange.py` returns JSON with:
```json
{
  "target_year": 2026,
  "total_posts": 38,
  "queries_used": [...],
  "posts": [
    {
      "title": "Show HN: Anonymous ephemeral notes for any location",
      "hn_url": "https://news.ycombinator.com/item?id=...",
      "points": 142,
      "num_comments": 87,
      "engagement_score": 316
    }
  ]
}
```

`engagement_score = points + num_comments * 2` — weight comments slightly for this topic,
as light exchange apps tend to generate discussion rather than pure upvotes.
