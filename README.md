# research-map-idea-skills

アプリ・Webサービスの**穴場アイデアを調査・発掘するためのローカルスキル**プロジェクトです。現在2つのリサーチスキルを収録しています。

Reddit のペインポイントと Hacker News の注目投稿を自動収集し、Claude がアイデアを分析・スコアリングしてレポートとして出力します。

---

## 収録スキル

| スキル | テーマ | キーワード例 |
|--------|--------|------------|
| **Skill 1** すれ違い通信調査 | Bluetooth・NFC・GPS を使った近接ソーシャル・出会い系コンテンツ | StreetPass、BLE、すれ違い、位置情報ゲーム |
| **Skill 2** ライト情報交換調査 | 匿名・使い捨て・低摩擦な情報共有アプリ | 匿名掲示板、エフェメラルノート、ピアQ&A |

両テーマを組み合わせたアイデア（例:「その場を通った人に匿名のメモを残せる」）も対応します。

---

## 使い方

このディレクトリで Claude Code を起動し、以下のように話しかけるだけです：

```
すれ違い通信アプリのアイデアを調査して
```

```
手軽に情報交換できるアプリのアイデアを探したい
```

```
2025年の匿名共有系コンテンツのトレンドを調べて
```

スキルが自動的に起動し、**調査対象年号と優先条件・制約（任意）を日本語で確認**した後、データ収集・分析・レポート生成まで自動で行います。条件を指定するとアイデア生成・スコアリングがその条件に沿った内容になります。

> 両スキルは **このディレクトリ内でのみ** 有効です（`CLAUDE.md` によるローカルスキル登録）。

---

## ディレクトリ構成

```
research-map-idea-skills/
│
├── CLAUDE.md                              # ローカルスキル登録・プロジェクト設定
├── SKILL.md                               # Skill 1: すれ違い通信調査
├── SKILL_light_exchange.md                # Skill 2: ライト情報交換調査
├── README.md                              # このファイル
│
├── scripts/
│   ├── fetch_reddit_proximity.py          # Reddit（すれ違い通信向け）
│   ├── fetch_hn_proximity.py              # HN（すれ違い通信向け）
│   ├── fetch_reddit_light_exchange.py     # Reddit（ライト情報交換向け）
│   ├── fetch_hn_light_exchange.py         # HN（ライト情報交換向け）
│   ├── fetch_reddit.py                    # 汎用 Reddit スクリプト（元ファイル）
│   └── fetch_hn.py                        # 汎用 HN スクリプト（元ファイル）
│
├── references/
│   ├── subreddits.md                      # Skill 1 サブレディット一覧
│   ├── hn_queries.md                      # Skill 1 HN クエリ一覧
│   ├── light_exchange_subreddits.md       # Skill 2 サブレディット一覧
│   ├── light_exchange_hn_queries.md       # Skill 2 HN クエリ一覧
│   ├── scoring_rubric.md                  # 共通: 5軸スコアリング基準
│   └── report_template.md                 # 共通: レポートテンプレート
│
└── reports/
    └── {year}/
        └── yyyy-mm-dd/
            └── HHMMSS.md                  # 生成されたリサーチレポート
```

---

## スキルの動作フロー（両スキル共通）

```
① 年号 + 条件確認（日本語で質問）
        ↓
② Reddit データ収集
   Skill 1: fetch_reddit_proximity.py   （25サブレディット・近接通信系）
   Skill 2: fetch_reddit_light_exchange.py（26サブレディット・情報交換系）
        ↓
③ Hacker News データ収集
   Skill 1: fetch_hn_proximity.py       （25クエリ・min-points 10）
   Skill 2: fetch_hn_light_exchange.py  （25クエリ・min-points 5）
   → 当年データが少ない場合は前年も補完
        ↓
④ データ分析
   - ペインポイントトップ抽出
   - Reddit × HN クロス参照
   - 「誰も作っていない空白地帯」の発見
   - 指定条件に関連するシグナルを注視
        ↓
⑤ アイデア生成（3〜5案）
   - テーマに合致する核となるメカニズムを持つ設計のみ提案
   - 条件に合うアイデアを優先。条件外でも有力なものは別掲
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

### Skill 1: すれ違い通信調査（25サブレディット）

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

**HN（25クエリ）:** `proximity app` / `StreetPass` / `BLE beacon` / `geofence social` など。詳細は [`references/hn_queries.md`](references/hn_queries.md) を参照。

---

### Skill 2: ライト情報交換調査（26サブレディット）

| カテゴリ | サブレディット |
|---------|-------------|
| カジュアル Q&A | r/AskReddit, r/NoStupidQuestions, r/tipofmytongue, r/explainlikeimfive |
| アイデア・思考共有 | r/Showerthoughts, r/mildlyinteresting, r/lifehacks |
| 匿名表現 | r/confession, r/offmychest, r/TrueOffMyChest |
| ハイパーローカル | r/Nextdoor |
| デジタルミニマリズム | r/nosurf, r/digitalminimalism, r/CasualConversation |
| 生産性・ノートツール | r/productivity, r/Notion, r/ObsidianMD |
| インディー開発 | r/SideProject, r/indiehackers, r/AppIdeas, r/androidapps, r/iosapps |
| コンテンツ発見 | r/InternetIsBeautiful |
| Q&A フォーマット参照 | r/personalfinance, r/legaladvice |

詳細は [`references/light_exchange_subreddits.md`](references/light_exchange_subreddits.md) を参照。

**HN（25クエリ）:** `ephemeral messaging` / `anonymous sharing app` / `local bulletin board` / `low friction sharing` など。詳細は [`references/light_exchange_hn_queries.md`](references/light_exchange_hn_queries.md) を参照。

---

## スクリプトの直接実行

Claude を介さず手動でデータ収集したい場合：

```bash
# Skill 1: Reddit（すれ違い通信向け）
python scripts/fetch_reddit_proximity.py --year 2026 --limit 30 --output /tmp/reddit_proximity.json

# Skill 1: Hacker News（すれ違い通信向け）
python scripts/fetch_hn_proximity.py --year 2026 --min-points 10 --output /tmp/hn_proximity.json

# Skill 2: Reddit（ライト情報交換向け）
python scripts/fetch_reddit_light_exchange.py --year 2026 --limit 30 --output /tmp/reddit_light.json

# Skill 2: Hacker News（ライト情報交換向け）
python scripts/fetch_hn_light_exchange.py --year 2026 --min-points 5 --output /tmp/hn_light.json

# カスタム指定の例
python scripts/fetch_reddit_light_exchange.py --year 2026 --subreddits "AskReddit,SideProject,AppIdeas"
python scripts/fetch_hn_light_exchange.py --year 2026 --queries "ephemeral messaging,anonymous notes app"
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
