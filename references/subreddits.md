# Subreddits for Proximity Communication Research

These subreddits are used by `scripts/fetch_reddit_proximity.py` to gather user pain points and trend signals relevant to proximity/encounter communication (すれ違い通信) app ideas.

## Location-Based Gaming & StreetPass Mechanics

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/pokemongo | Pokémon GO community | Proximity mechanics, real-world encounter features, event requests |
| r/Ingress | Ingress (Niantic) | Hyperlocal gameplay, portal/encounter mechanics |
| r/NianticWayfarer | Niantic waypoint review | Location-based game design feedback |
| r/streetpass | Nintendo 3DS StreetPass | Classic encounter-communication UX, nostalgia-driven demand |

## Proximity-Based Social & Dating

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/Tinder | Dating via location | Location-based matching pain points, feature gaps |
| r/Bumble | Dating & networking | Women-first proximity networking, BFF/bizz modes |
| r/hinge | Relationship-focused dating | Serendipitous encounter requests, UX frustrations |
| r/dating_advice | Dating tips & frustrations | Real unmet needs around meeting people IRL |
| r/socialskills | Social interaction help | Anxiety around in-person encounters, tech-assisted icebreaking |

## Bluetooth, NFC & Local Networking

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/bluetooth | Bluetooth tech discussions | BLE proximity use cases, technical pain points |
| r/NFC | Near Field Communication | Tap-to-connect ideas, business card replacement use cases |
| r/IoT | Internet of Things | Sensor-based proximity apps, wearable encounters |
| r/embedded | Embedded systems | Low-power proximity beacon hardware discussions |

## Hyperlocal & Community Apps

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/Nextdoor | Neighborhood social network | Hyperlocal community pain points, neighbor discovery |
| r/digitalnomad | Remote workers traveling | Meeting people in coworking spaces, travel encounters (loneliness in new cities) |

## Privacy & Concerns

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/privacy | Privacy advocacy | User concerns about location tracking, opt-in/opt-out desires |
| r/privacytoolsIO | Privacy tools | Technical users' proximity tracking concerns = design constraints |

## Wearables & Hardware

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/wearables | Wearable device discussion | Wearable proximity communication concepts (e.g., badge, watch) |
| r/smartwatch | Smartwatch community | Watch-based encounter UX potential |

## Indie Dev & Startup

| Subreddit | Focus | Why Relevant |
|-----------|-------|-------------|
| r/startups | Startup community | Niche app opportunity discussions |
| r/Entrepreneur | Entrepreneurs | Unserved market signals |
| r/SideProject | Solo dev projects | What independent developers are building in this space |
| r/indiehackers | Indie hackers | Bootstrapped proximity apps, revenue models |
| r/androidapps | Android app discussion | Feature requests, gaps in existing location apps |
| r/iosapps | iOS app discussion | Same for iOS ecosystem |

---

## Adding New Subreddits

To add subreddits to the default list, edit the `PROXIMITY_SUBREDDITS` list in `scripts/fetch_reddit_proximity.py`. You can also pass them at runtime:

```bash
python scripts/fetch_reddit_proximity.py --year 2026 \
  --subreddits "pokemongo,streetpass,Tinder" \
  --output /tmp/reddit_proximity_raw.json
```
