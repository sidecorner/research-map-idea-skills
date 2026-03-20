# Report Template

Reports are saved to: `reports/{year}/{yyyymmdd}/{hhmmss}.md`

Example path: `reports/2026/20260314/143022.md`

---

## Template

```markdown
# {report_title}アイデア調査レポート
<!-- report_title: proximity → "すれ違い通信", light exchange → "ライトな情報交換" -->

**調査テーマ:** {report_title}
**調査対象年号:** {year}
**調査期間:** {start_date} 〜 {end_date}（直近1年間 or {year}年通年）
**調査日時:** {datetime}
**データソース:** Reddit ({subreddits_count} subreddits) / Hacker News ({hn_queries_count} queries) / Qiita ({qiita_queries_count} queries) / Indie Hackers (Firebase REST API)
**指定条件:** {constraints（なし の場合は「なし」）}

---

## 再現用プロンプト

このレポートと同じ条件で再調査したい場合は、以下のプロンプトをそのまま使用してください。

```
{reusable_prompt — 調査条件を簡潔にまとめた再現用プロンプト。
「〇〇のアイデアを調査してください。条件: …」形式で、
年号・制約・除外事項・重点テーマを1〜3文にまとめる。
ユーザーの言葉を引用しつつ、検索に有効な形に整理すること。}
```

---

## エグゼクティブサマリー

{1–3 sentences summarizing the most notable trend signals and top idea recommendations}

---

## Reddit 調査結果

### ペインポイント トップ10

{Table or list of top pain-point posts by engagement, with title, subreddit, score, and URL}

### トレンドシグナル

{2–3 patterns or recurring themes observed across posts}

---

## Hacker News 調査結果

### 注目投稿 トップ10

{Table of top HN posts by engagement_score, with title, points, comments, HN URL}

### エンジニア/起業家の関心領域

{2–3 themes from HN that indicate technical or market interest}

---

## Qiita 調査結果

### 注目記事 トップ10

{Table of top Qiita articles by engagement_score (likes + comments×2), with title, likes, tags, URL}

### 日本語開発者コミュニティの関心領域

{2–3 themes from Qiita that reflect Japanese developer experience and pain points}

---

## Indie Hackers 調査結果

### 注目投稿 トップ10

{Table of top IH posts by engagement_score (replies×10 + link_clicks×3 + views×0.01), with title, replies, views, group, URL}

### インディー開発者の関心領域

{2–3 themes from IH that reveal solo-founder pain points, niche ideas, or early-stage validation signals}

---

## アイデア提案

For each idea, include the following structure:

---

### アイデア {N}: {idea name}

**概要**
{1–2 paragraph description of the idea, what problem it solves, and who it's for}

**コアメカニクス**
{Proximity skill: How proximity/encounter communication is the core mechanic — e.g., BLE passive discovery, location check-in, event-based encounter, QR/NFC tap}
{Light exchange skill: What makes the exchange feel "light" — specifically how friction is reduced compared to full social platforms}

**根拠となるユーザーの声**
{1–3 specific Reddit posts, HN threads, Qiita articles, or IH posts that validate this pain point or demand}

**スコア評価**

| Dimension          | Score | Notes |
|--------------------|-------|-------|
| 実現可能性          | ⭐⭐⭐⭐  | {brief note} |
| 開発期間            | ⭐⭐⭐   | {brief note} |
| 収益性              | ⭐⭐⭐   | {brief note} |
| 競合優位性          | ⭐⭐⭐⭐  | {brief note} |
| 小規模開発適性      | ⭐⭐⭐⭐  | {brief note} |
| **総合スコア**      | **XX/25** | |

**推奨アクション**
{One concrete next step: e.g., "Build a web prototype for conference use cases", "Validate with 10 potential users in target community"}

---

## 総合比較

| アイデア | 実現可能性 | 開発期間 | 収益性 | 競合優位性 | 小規模適性 | 総合 |
|---------|-----------|---------|-------|----------|-----------|------|
| {N}: {name} | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 18/25 |

## 優先推奨順位

1. 🟢 **{idea name}** (XX/25) — {one sentence why}
2. 🟡 **{idea name}** (XX/25) — {one sentence why}
3. 🟠 **{idea name}** (XX/25) — {one sentence why}

---

*このレポートは {skill_name} スキルにより自動生成されました。データソース: Reddit / Hacker News / Qiita*
```

---

## File Naming Convention

- Directory: `reports/{year}/{yyyymmdd}/`  ← date has NO dashes (e.g. `20260314`)
- Filename: `{hhmmss}.md` — 24-hour, no separators (e.g. `143022.md` for 14:30:22)
- Full example: `reports/2026/20260314/143022.md`

The report file must be created **after** completing the research and analysis, not before.
