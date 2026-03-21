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

## ゲーム性の強弱パターン

アイデアを「ゲーム性の強さ」で分類すると、ユーザーの好みや用途に合わせた提案ができる。
ゲーム性が強いほど継続動機が外発的・数値的になり、弱いほど体験の質と偶発性が動機の核になる。

### ゲーム性レベル定義

| レベル | 特徴 | 向いているユーザー |
|--------|------|--------------------|
| **強い** | ポイント・レアリティ・ビンゴ・クエスト・ランキング・達成バッジ | ゲーム習慣のあるユーザー・ゲーミフィケーションを積極採用したい場合 |
| **中程度** | 「届いた件数」統計・コレクション図鑑・連鎖カウント・ルートバッジ | ゲームほどではないが数字の変化で継続できるユーザー |
| **弱い** | 「届いた」通知のみ・感謝ボタン1種・自然な give & take | 情報交換そのものが目的のユーザー・ゲーム疲れしたユーザー |

### スコアリング調整

ゲーム性を抑える制約が指定された場合:
- **除外する要素**: スコア・ポイント・レアリティ・達成ゴール（ビンゴ等）・ランキング・競争
- **残せる要素**: 「届いた」通知・1種類のみのリアクション（感謝ボタン等）・自然な互助設計（書かないと読めない等）
- **注意点**: ゲーム性がないとコールドスタート問題がより深刻になる。特定イベント・場所でのクローズドβから開始すること。「届いた通知の文言・タイミング」が唯一の外発的動機になるため、この設計に開発リソースを集中させること。

### 過去アイデアのゲーム性分類例（参考）

| ゲーム性 強い | ゲーム性 中程度 | ゲーム性 弱い |
|-------------|--------------|-------------|
| PassBingo（ビンゴ達成） | ChipWalk（レアリティ・図鑑） | HandNote（引き継ぎ通知のみ） |
| QuestWalk（デイリークエスト） | RelayBaton（連鎖カウント） | TipDrop（届いた通知のみ） |
| KnowLink（クレジット経済） | SkillSpot（マッチング） | NowNote（感謝ボタン1種） |
| | SpotBoard / LocalTips / PassNote / TrailNote | RouteNote（返事1回のみ） |

---

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
