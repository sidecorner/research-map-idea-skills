# Idea Patterns and Constraint Guide

## What Makes a Good Idea

Each idea must:
1. Have a clear **proximity/encounter mechanic** or **lightweight exchange mechanic** at its core
2. Solve a **specific friction point** evidenced by the data
3. Be realistically buildable by a small team or solo developer

## Good Idea Patterns

- **Passive discovery**: "You walked past 3 people who share your interest in X" — no action required
- **Event-based encounters**: proximity features that activate during conferences, concerts, local events
- **Ephemeral community boards**: Notes or tips that expire — no permanent record, no follower counts
- **Context-triggered sharing**: Leave a note tied to a place or object that others discover passively
- **Gamified encounters**: StreetPass-style collections, stamps, or artifacts from physical meetups
- **Physical-digital bridges**: QR systems or BLE devices as carriers of exchange (NFC excluded)
- **Anonymous peer Q&A**: Ask anything without an account; community answers without identity pressure
- **Map-anchored content**: GPS or map SDK (Mapbox, Google Maps) as the discovery surface

## Applying User Constraints

If `{constraints}` were specified:
- **Prioritize** ideas that naturally fit. Lead with those.
- **Don't force compliance.** If data strongly points to a high-potential idea outside the constraints, include it as a separate "制約外だが注目" section.
- **Note trade-offs honestly.**

### Constraint-Specific Scoring Adjustments

| Constraint | Adjustment |
|-----------|-----------|
| iOS向け | Lower 実現可能性 for ideas relying on BLE background scanning (OS-restricted) |
| ソロ開発 | Weight 小規模開発適性 heavily; flag infra-heavy ideas |
| 日本市場 | Consider LINE integration, commuter culture, StreetPass nostalgia |
| B2B SaaS | Favor ideas with identifiable business buyers (event organizers, venues, HR) |
| 匿名性重視 | Favor ephemeral/no-account designs; flag identity-linked approaches |
| Google Maps/Mapbox使用 | Include map visualization as the core discovery UX; reference Radar.com for geofencing |
