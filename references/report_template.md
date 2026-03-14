# Report Template

Reports are saved to: `reports/{year}/yyyy-mm-dd/HHMMSS.md`

Example path: `reports/2026/2026-03-14/143022.md`

---

## Template

```markdown
# すれ違い通信アイデア調査レポート

**調査対象年号:** {year}
**調査日時:** {datetime}
**データソース:** Reddit ({subreddits_count} subreddits) / Hacker News ({hn_queries_count} queries)
**指定条件:** {constraints（なし の場合は「なし」）}

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

## アイデア提案

For each idea, include the following structure:

---

### アイデア {N}: {idea name}

**概要**
{1–2 paragraph description of the idea, what problem it solves, and who it's for}

**すれ違い通信の活用方法**
{How proximity/encounter communication is the core mechanic — e.g., BLE passive discovery, location check-in, event-based encounter, QR/NFC tap}

**根拠となるユーザーの声**
{1–3 specific Reddit posts or HN threads that validate this pain point or demand}

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

*このレポートは proximity-communication-idea-research スキルにより自動生成されました。*
```

---

## File Naming Convention

- Directory: `reports/{year}/{yyyy-mm-dd}/`
- Filename: `{HHMMSS}.md` (24-hour format, no separators)
- Example: `reports/2026/2026-03-14/143022.md`

The report file must be created **after** completing the research and analysis, not before.
