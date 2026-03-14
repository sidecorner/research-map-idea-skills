# Subreddits for Light Information Exchange Research

These subreddits are used by `scripts/fetch_reddit_light_exchange.py` to gather user pain points
and trend signals relevant to casual/lightweight information exchange app ideas.

## Casual Q&A and Knowledge Sharing

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/AskReddit | Broad casual Q&A | The canonical low-friction "ask anyone anything" format — core UX to study |
| r/NoStupidQuestions | Low-barrier Q&A | Users who need info but fear judgment; demand for anonymous or judgment-free channels |
| r/tipofmytongue | Help identifying things | "I know something exists but can't name it" — peer-assisted recall use case |
| r/explainlikeimfive | Simple explanations | Demand for digestible, accessible information exchange |

## Lightweight Idea and Thought Sharing

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/Showerthoughts | Casual observations | Low-stakes thought sharing; tone reference for "light" content |
| r/mildlyinteresting | Everyday discoveries | Ambient, serendipitous content discovery model |
| r/lifehacks | Practical tips | Peer-generated micro-knowledge; tip-passing culture |

## Anonymous and Low-Barrier Expression

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/confession | Anonymous personal sharing | Demand for zero-identity expression; pain around identity-linked sharing |
| r/offmychest | Anonymous venting | Same as above; also signals "I just need to say this somewhere" use case |
| r/TrueOffMyChest | Anonymous expression | Stricter rules version; illustrates moderation needs for anonymous platforms |

## Hyperlocal Information Exchange

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/Nextdoor | Neighborhood social | Hyperlocal info pain points: noise, trust issues, info overload in local networks |

## Digital Minimalism and Lightweight Tool Demand

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/nosurf | Reducing heavy social media | Users actively seeking lighter, less addictive alternatives |
| r/digitalminimalism | Minimalist digital life | Design preference signals: what makes tools feel "light" vs. "heavy" |
| r/CasualConversation | Low-stakes chat | The demand for conversation without agenda — informational equivalent |

## Productivity and Note-Taking Tools

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/productivity | Productivity tools | Quick capture, brain dump, and sharing tools; friction points in current tools |
| r/Notion | Notion community | Sharing structured lightweight info; templates and micro-databases |
| r/ObsidianMD | Obsidian community | Local-first, low-friction note sharing; privacy-conscious users |

## Indie Dev and App Discovery

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/SideProject | Solo dev projects | What independent developers are building in lightweight sharing |
| r/indiehackers | Bootstrapped apps | Revenue models for light exchange apps; what works at small scale |
| r/AppIdeas | App concept discussion | Raw, unfiltered demand signals from users who "wish an app existed" |
| r/androidapps | Android app discovery | Feature requests and gaps in existing sharing/note apps |
| r/iosapps | iOS app discovery | Same for iOS ecosystem |

## Content Discovery

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/InternetIsBeautiful | Lightweight web discoveries | Apps/sites that feel effortless and surprising = design target |

## Community Q&A Format Reference

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/personalfinance | Finance Q&A | High-quality peer advice exchange format; trust and authority signals |
| r/legaladvice | Legal Q&A | Domain-specific peer exchange; trust/verification challenges |

---

## Adding New Subreddits

Edit `LIGHT_EXCHANGE_SUBREDDITS` in `scripts/fetch_reddit_light_exchange.py`, or pass at runtime:

```bash
python scripts/fetch_reddit_light_exchange.py --year 2026 \
  --subreddits "AskReddit,NoStupidQuestions,SideProject" \
  --output /tmp/reddit_light_raw.json
```
