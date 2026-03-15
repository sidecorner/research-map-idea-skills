# Idea Scoring Rubric (Proximity Communication / Light Exchange)

Each idea discovered through research is scored on five dimensions using a 1–5 scale. These scores help quickly compare ideas and prioritize which ones are worth pursuing for solo or small-team development.

---

## Scoring Dimensions

### 1. 実現可能性 (Feasibility) — Technical buildability

How straightforward is it to build a working MVP?

| Score | Meaning |
|-------|---------|
| ⭐ 1 | Requires unproven tech, significant R&D, or hardware development |
| ⭐⭐ 2 | Technically complex; needs specialized expertise or large team |
| ⭐⭐⭐ 3 | Buildable but requires moderate effort; some tricky components |
| ⭐⭐⭐⭐ 4 | Mostly standard tech (BLE, WebSockets, GPS); clear implementation path |
| ⭐⭐⭐⭐⭐ 5 | Simple stack, well-documented APIs, minimal infrastructure needed |

**Proximity-specific considerations:**
- Background BLE scanning has OS restrictions (iOS especially)
- Real-time location sharing raises battery and permission challenges
- P2P/mesh apps without server are harder to debug and monetize

---

### 2. 開発期間 (Development Time) — Speed to shippable MVP

How quickly can a solo dev or small team launch a testable version?

| Score | Meaning |
|-------|---------|
| ⭐ 1 | 12+ months to a meaningful MVP |
| ⭐⭐ 2 | 6–12 months |
| ⭐⭐⭐ 3 | 3–6 months |
| ⭐⭐⭐⭐ 4 | 1–3 months |
| ⭐⭐⭐⭐⭐ 5 | Under 1 month (e.g., web app + simple backend) |

**Note:** Score reflects MVP launch speed, not full feature parity with incumbents.

---

### 3. 収益性 (Profitability) — Revenue potential

How likely is this to generate sustainable revenue?

| Score | Meaning |
|-------|---------|
| ⭐ 1 | Very hard to monetize; free-only or ad-dependent niche |
| ⭐⭐ 2 | Weak monetization signals; relies on scale |
| ⭐⭐⭐ 3 | Plausible revenue path (freemium, event-based fees, B2B niche) |
| ⭐⭐⭐⭐ 4 | Clear willingness to pay; subscription or transactional model viable |
| ⭐⭐⭐⭐⭐ 5 | Strong commercial pull; enterprise or marketplace potential |

**Proximity-specific monetization patterns:**
- Event organizers paying for proximity networking tools
- B2B badges/wearables for conferences
- Premium unlock for extended encounter features
- Data-anonymized analytics for venue operators

---

### 4. 競合優位性 (Competitive Advantage) — Differentiation

How defensible is this idea against existing products and copycats?

| Score | Meaning |
|-------|---------|
| ⭐ 1 | Crowded market; dominated by well-funded incumbents (e.g., Tinder) |
| ⭐⭐ 2 | Some existing solutions; hard to differentiate meaningfully |
| ⭐⭐⭐ 3 | Underserved segment with moderate competition |
| ⭐⭐⭐⭐ 4 | Niche or context-specific; limited direct competitors |
| ⭐⭐⭐⭐⭐ 5 | Unique mechanic or community niche with no clear rival |

**Factors that create advantage in proximity apps:**
- Community lock-in (network effects around a specific hobby/interest)
- Unique hardware integration (wearable, badge)
- Context specificity (conferences, travel hostels, museums)
- Privacy-first design when others are invasive

---

### 5. 小規模開発適性 (Small-Team Suitability) — How well it fits solo/indie development

Can this be built and operated by a 1–3 person team without VC funding?

| Score | Meaning |
|-------|---------|
| ⭐ 1 | Requires large team, expensive infrastructure, or regulatory compliance |
| ⭐⭐ 2 | Significant operational burden (moderation, real-time infra, hardware) |
| ⭐⭐⭐ 3 | Manageable with some automation; some scaling challenges |
| ⭐⭐⭐⭐ 4 | Fits indie dev well; predictable costs, manageable support |
| ⭐⭐⭐⭐⭐ 5 | Ideal for solo/indie: serverless-friendly, async, niche audience |

---

## Score Summary Format

In the report, present scores as a table and calculate a weighted total:

```markdown
| Dimension          | Score | Notes                          |
|--------------------|-------|--------------------------------|
| 実現可能性          | ⭐⭐⭐⭐  | Standard BLE + WebSocket stack |
| 開発期間            | ⭐⭐⭐⭐  | ~2 months to MVP               |
| 収益性              | ⭐⭐⭐   | Event B2B potential            |
| 競合優位性          | ⭐⭐⭐⭐  | No direct rival in this niche  |
| 小規模開発適性      | ⭐⭐⭐⭐⭐ | Serverless + niche audience    |
| **総合スコア**      | **21/25** |                             |
```

## Score Interpretation

| Total | Recommendation |
|-------|----------------|
| 22–25 | 🟢 Strong candidate — prioritize |
| 17–21 | 🟡 Promising — worth prototyping |
| 12–16 | 🟠 Conditional — needs validation or pivot |
| < 12  | 🔴 Risky — reconsider or table |
