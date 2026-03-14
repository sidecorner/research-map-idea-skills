# research-map-idea-skills

すれ違い通信（proximity/encounter communication）機能を持つアプリ・Webサービスの**穴場アイデアを調査・発掘するためのローカルスキル**プロジェクトです。

Reddit のペインポイントと Hacker News の注目投稿を自動収集し、Claude がアイデアを分析・スコアリングしてレポートとして出力します。

---

## 使い方

このディレクトリで Claude Code を起動し、以下のように話しかけるだけです：

```
すれ違い通信アプリのアイデアを調査して
```

```
2025年のすれ違い通信系コンテンツのトレンドを調べて
```

スキルが自動的に起動し、**調査対象年号を日本語で確認**した後、データ収集・分析・レポート生成まで自動で行います。

> このスキルは **このディレクトリ内でのみ** 有効です（`CLAUDE.md` によるローカルスキル登録）。

---

## ディレクトリ構成

```
research-map-idea-skills/
│
├── CLAUDE.md                        # ローカルスキル登録・プロジェクト設定
├── SKILL.md                         # スキル定義本体（Claude が参照）
├── README.md                        # このファイル
│
├── scripts/
│   ├── fetch_reddit_proximity.py    # Reddit データ収集（すれ違い通信向け）
│   ├── fetch_hn_proximity.py        # Hacker News データ収集（すれ違い通信向け）
│   ├── fetch_reddit.py              # Reddit 汎用スクリプト（元ファイル）
│   └── fetch_hn.py                  # HN 汎用スクリプト（元ファイル）
│
├── references/
│   ├── subreddits.md                # 調査対象サブレディット一覧と選定理由
│   ├── hn_queries.md                # HN 検索クエリ一覧と設計メモ
│   ├── scoring_rubric.md            # アイデアスコアリング基準（5軸）
│   └── report_template.md          # レポート出力テンプレート
│
└── reports/
    └── {year}/
        └── yyyy-mm-dd/
            └── HHMMSS.md           # 生成されたリサーチレポート
```

---

## スキルの動作フロー

```
① 年号確認（日本語で質問）
        ↓
② Reddit データ収集
   scripts/fetch_reddit_proximity.py
   → 25サブレディット・各30件取得
   → ペインポイント・近接関連フラグ付き
        ↓
③ Hacker News データ収集
   scripts/fetch_hn_proximity.py
   → 25クエリ・min-points 10 でフィルタ
   → 当年データが少ない場合は前年も補完
        ↓
④ データ分析
   - ペインポイントトップ10の抽出
   - Reddit × HN のクロス参照
   - 「誰も作っていない空白地帯」の発見
        ↓
⑤ アイデア生成（3〜5案）
   - 近接通信が核にある設計のみ提案
   - 実データ（投稿URL）を根拠として引用
        ↓
⑥ 5軸スコアリング
   実現可能性 / 開発期間 / 収益性 / 競合優位性 / 小規模開発適性
        ↓
⑦ レポート出力
   reports/{year}/yyyy-mm-dd/HHMMSS.md
```

---

## スコアリング基準（5軸・各5段階）

| 軸 | 評価内容 |
|----|---------|
| **実現可能性** | 技術的な構築しやすさ。既存 API・標準スタックで実装できるか |
| **開発期間** | MVP を出せる速さ。5 = 1ヶ月未満、1 = 12ヶ月以上 |
| **収益性** | 持続的な収益モデルが描けるか（サブスク・B2B・イベント課金など）|
| **競合優位性** | 差別化の強さ。既存サービスが手薄なニッチをとれるか |
| **小規模開発適性** | 1〜3人チームで運用可能か。インフラ・モデレーション負荷を含む |

**総合スコア判定：**
- 🟢 22–25点：強力候補、即着手推奨
- 🟡 17–21点：有望、検証価値あり
- 🟠 12–16点：要検証または方向転換
- 🔴 12点未満：リスク高、再考推奨

詳細は [`references/scoring_rubric.md`](references/scoring_rubric.md) を参照。

---

## 調査対象データソース

### Reddit（25サブレディット）

カテゴリ別の主な対象：

| カテゴリ | サブレディット |
|---------|-------------|
| 位置情報ゲーム | r/pokemongo, r/Ingress, r/NianticWayfarer, r/streetpass |
| 近接ソーシャル・マッチング | r/Tinder, r/Bumble, r/hinge, r/dating_advice |
| BLE / NFC / IoT | r/bluetooth, r/NFC, r/IoT, r/embedded |
| ハイパーローカル | r/Nextdoor, r/digitalnomad |
| プライバシー | r/privacy, r/privacytoolsIO |
| ウェアラブル | r/wearables, r/smartwatch |
| インディー開発 | r/SideProject, r/indiehackers, r/startups, r/Entrepreneur |
| アプリ全般 | r/androidapps, r/iosapps |

詳細は [`references/subreddits.md`](references/subreddits.md) を参照。

### Hacker News（25クエリ）

`proximity app` / `StreetPass` / `BLE beacon` / `geofence social` / `serendipitous encounters` など、すれ違い通信に直接関連するクエリで高評価投稿を収集。

詳細は [`references/hn_queries.md`](references/hn_queries.md) を参照。

---

## スクリプトの直接実行

Claude を介さず手動でデータ収集したい場合：

```bash
# Reddit（すれ違い通信向け）
python scripts/fetch_reddit_proximity.py --year 2026 --limit 30 --output /tmp/reddit_out.json

# Hacker News（すれ違い通信向け）
python scripts/fetch_hn_proximity.py --year 2026 --min-points 10 --output /tmp/hn_out.json

# カスタムサブレディットを指定
python scripts/fetch_reddit_proximity.py --year 2026 --subreddits "pokemongo,streetpass,NFC"

# カスタムクエリを指定
python scripts/fetch_hn_proximity.py --year 2026 --queries "proximity app,NFC social"
```

いずれも認証不要（Reddit Public JSON API / HN Algolia API を使用）。

---

## レポート出力先

```
reports/
└── 2026/
    └── 2026-03-14/
        └── 204906.md   ← 2026-03-14 20:49:06 に生成されたレポート
```

同一日に複数回実行すると、時刻の異なるファイルが追記されていきます。

---

## 注意事項

- **ローカル限定**: このスキルは `CLAUDE.md` によりこのディレクトリ内でのみ有効です
- **当年データの少なさ**: 年初に実行すると HN 投稿数が少ない場合があります。スクリプトは自動で前年データを補完します
- **API 制限**: Reddit / HN ともに公開 API のため認証不要ですが、レート制限対策として各サブレディット間に 1 秒のスリープを入れています
