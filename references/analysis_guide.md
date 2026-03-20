# Data Analysis Guide

## Reddit

- **Primary:** `top_combined_posts` — posts that are BOTH pain points AND relevant. Highest signal.
- **Secondary:** `top_relevant_posts` — broader topical discussions without explicit pain signals
- **Tertiary:** `top_pain_points` — all pain keywords (may include off-topic viral posts; background context only)
- Look for: "I just want a simple way to…", "why is there no app that…", recurring unmet needs

## Hacker News

- Focus on posts with high `engagement_score` (points + 2× comments)
- Show HN posts (builders), Ask HN (demand), post-mortems (what failed) are all valuable
- High comment counts with controversial tone often reveal structural tensions

## Qiita

- Read the `items` array (key is `items`, not `articles`)
- Focus on high `engagement_score` (likes + 2× comments)
- "やってみた" / "作ってみた" articles reveal implementation pain points
- Note popular tags — they indicate active interest areas in the Japanese dev community
- Qiita often surfaces mobile-first, Japan-specific UX considerations that Reddit misses

## Indie Hackers

- Read the `posts` array (key is `posts`)
- Focus on high `engagement_score` (replies × 10 + link_clicks × 3 + views × 0.01)
- `group` field indicates topic category (e.g., "Developers", "Digital Nomads", "Growth")
- IH posts often reveal solo-founder pain points, monetization strategies, and niche ideas earlier than HN
- Look for: "I built X and here's what happened", "Looking for a partner to build Y", "Micro-SaaS for Z"
- IH skews toward English-speaking indie devs and is particularly strong on niche app ideas and early-stage validation

## Cross-Reference Patterns

- Do Reddit users want something that HN builders have tried but abandoned?
- Does Qiita show Japanese developers hitting technical blockers that suggest an underserved niche?
- What pain points appear across multiple communities AND on Qiita? (= strong cross-market signal)
- What is completely absent from all three sources? (= no one has tried it yet)
