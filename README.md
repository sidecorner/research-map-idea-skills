# research-map-idea-skills

アプリ・Webサービスの**穴場アイデアを調査・発掘するためのローカルスキル**プロジェクトです。現在2つのリサーチスキルを収録しています。

Reddit のペインポイント・Hacker News の注目投稿・Qiita の日本語開発者記事を自動収集し、Claude がアイデアを分析・スコアリングしてレポートとして出力します。

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

> **調査期間の自動決定:** 今年を指定した場合（または指定なし）は直近1年間（ローリングウィンドウ）を対象にします。過去の年を指定した場合はその年の1月1日〜12月31日を対象にします。

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
│   ├── fetch_hn_proximity.py              # HN（すれ違い通信向け、--rolling 対応）
│   ├── fetch_qiita_proximity.py           # Qiita（すれ違い通信向け、--rolling 対応）
│   ├── fetch_reddit_light_exchange.py     # Reddit（ライト情報交換向け）
│   ├── fetch_hn_light_exchange.py         # HN（ライト情報交換向け、--rolling 対応）
│   ├── fetch_qiita_light_exchange.py      # Qiita（ライト情報交換向け、--rolling 対応）
│   ├── fetch_reddit.py                    # 汎用 Reddit スクリプト（元ファイル）
│   └── fetch_hn.py                        # 汎用 HN スクリプト（元ファイル）
│
├── references/
│   ├── subreddits.md                      # Skill 1 サブレディット一覧
│   ├── hn_queries.md                      # Skill 1 HN クエリ一覧
│   ├── qiita_queries_proximity.md         # Skill 1 Qiita クエリ一覧
│   ├── light_exchange_subreddits.md       # Skill 2 サブレディット一覧
│   ├── light_exchange_hn_queries.md       # Skill 2 HN クエリ一覧
│   ├── qiita_queries_light_exchange.md    # Skill 2 Qiita クエリ一覧
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
   → 今年指定 or 無指定: 直近1年間（ローリングウィンドウ）を使用
   → 過去年指定: その年の 01-01〜12-31 を使用
        ↓
② Reddit データ収集
   Skill 1: fetch_reddit_proximity.py    （25サブレディット・近接通信系）
   Skill 2: fetch_reddit_light_exchange.py（26サブレディット・情報交換系）
        ↓
③ Hacker News データ収集
   Skill 1: fetch_hn_proximity.py        （25クエリ・min-points 5）
   Skill 2: fetch_hn_light_exchange.py   （25クエリ・min-points 5）
   → 結果が少ない場合は前年も補完
        ↓
④ Qiita データ収集
   Skill 1: fetch_qiita_proximity.py     （12クエリ・日本語開発者コミュニティ）
   Skill 2: fetch_qiita_light_exchange.py（12クエリ・日本語開発者コミュニティ）
        ↓
⑤ データ分析
   - ペインポイントトップ抽出
   - Reddit × HN × Qiita クロス参照
   - 「誰も作っていない空白地帯」の発見
   - 指定条件に関連するシグナルを注視
        ↓
⑥ アイデア生成（3〜5案）
   - テーマに合致する核となるメカニズムを持つ設計のみ提案
   - 条件に合うアイデアを優先。条件外でも有力なものは別掲
   - 実データ（投稿URL / 記事URL）を根拠として引用
        ↓
⑦ 5軸スコアリング
   実現可能性 / 開発期間 / 収益性 / 競合優位性 / 小規模開発適性
        ↓
⑧ レポート出力
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

3つのソースからデータを収集し、英語圏ユーザーの声・グローバルビルダーの動向・日本語開発者の実装経験を横断的に分析します。

| ソース | 特性 |
|--------|------|
| **Reddit** | 英語圏ユーザーのペインポイント・フィーチャーリクエスト |
| **Hacker News** | グローバルなビルダー・起業家の市場関心・技術動向 |
| **Qiita** | 日本語開発者コミュニティの実装経験・技術的障壁 |

---

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

**Qiita（12クエリ）:** `tag:BLE` / `tag:NFC` / `title:すれ違い` / `title:BLE 近接` など。詳細は [`references/qiita_queries_proximity.md`](references/qiita_queries_proximity.md) を参照。

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

**Qiita（12クエリ）:** `tag:匿名` / `tag:掲示板` / `title:匿名 投稿` / `title:軽量 情報共有` など。詳細は [`references/qiita_queries_light_exchange.md`](references/qiita_queries_light_exchange.md) を参照。

---

## セットアップ（初回のみ）

### Qiita アクセストークンの設定

Qiita の検索には個人アクセストークンが必要です（レート制限 60→1000 req/時）。

**1. トークンを発行する**
Qiita アカウントにログイン → 設定 → アプリケーション → 個人用アクセストークン
- スコープ: `read_qiita` のみにチェック
- トークン名: 任意（例: `research-map-idea-skills`）

**2. トークンファイルに保存する（推奨・Claude Code でも自動適用）**
```bash
mkdir -p ~/.config/qiita
echo "your_token_here" > ~/.config/qiita/token
chmod 600 ~/.config/qiita/token  # 自分だけ読み取れるようにする
```

**3. 確認**
```bash
cat ~/.config/qiita/token  # トークンが表示されれば OK
```

設定後はスクリプト実行時に `--token` 指定不要。自動的に読み込まれます。

**優先順位（3通りの指定方法）**

| 優先度 | 方法 | 用途 |
|--------|------|------|
| 1 | `--token YOUR_TOKEN` | 一時的な上書き |
| 2 | `export QIITA_TOKEN=xxx` in `~/.zshrc` | 端末での手動実行 |
| 3 | `~/.config/qiita/token` ファイル | **Claude Code 経由での自動実行（推奨）** |

> ⚠ トークンをこのプロジェクトのファイルには絶対に書かないでください（`.gitignore` で `.env` 等は除外済みですが、誤って `SKILL.md` 等に書き込むと漏洩します）。

---

## スクリプトの直接実行

Claude を介さず手動でデータ収集したい場合：

```bash
# ──────────────────────────────────────────
# Skill 1: すれ違い通信向け
# ──────────────────────────────────────────

# Reddit
python scripts/fetch_reddit_proximity.py --year 2026 --limit 30 --output /tmp/reddit_proximity.json

# Hacker News（カレンダー年）
python scripts/fetch_hn_proximity.py --year 2025 --min-points 5 --output /tmp/hn_proximity.json

# Hacker News（直近1年ローリング）
python scripts/fetch_hn_proximity.py --rolling --min-points 5 --output /tmp/hn_proximity_rolling.json

# Qiita（カレンダー年）※ QIITA_TOKEN 環境変数が自動適用される
python scripts/fetch_qiita_proximity.py --year 2025 --output /tmp/qiita_proximity.json

# Qiita（直近1年ローリング）
python scripts/fetch_qiita_proximity.py --rolling --output /tmp/qiita_proximity_rolling.json

# ──────────────────────────────────────────
# Skill 2: ライト情報交換向け
# ──────────────────────────────────────────

# Reddit
python scripts/fetch_reddit_light_exchange.py --year 2026 --limit 30 --output /tmp/reddit_light.json

# Hacker News（カレンダー年）
python scripts/fetch_hn_light_exchange.py --year 2025 --min-points 5 --output /tmp/hn_light.json

# Hacker News（直近1年ローリング）
python scripts/fetch_hn_light_exchange.py --rolling --min-points 5 --output /tmp/hn_light_rolling.json

# Qiita（直近1年ローリング）※ QIITA_TOKEN 環境変数が自動適用される
python scripts/fetch_qiita_light_exchange.py --rolling --output /tmp/qiita_light_rolling.json

# カスタム指定の例
python scripts/fetch_reddit_light_exchange.py --year 2026 --subreddits "AskReddit,SideProject,AppIdeas"
python scripts/fetch_hn_light_exchange.py --rolling --queries "ephemeral messaging,anonymous notes app"
python scripts/fetch_qiita_proximity.py --rolling --queries "すれ違い通信,BLE 近接,NFC"
```

Reddit / HN は認証不要（公開 API）。Qiita は認証なしで 60 req/hour、トークンあり（無料）で 1000 req/hour。

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
- **調査期間の自動決定**: 今年を指定した場合は直近1年間（ローリング）を使用。前年以前を指定した場合はその年の通年を使用します
- **当年データの少なさ**: 年初に実行すると HN 投稿数が少ない場合があります。スクリプトは自動で前年データを補完します
- **Reddit / HN の API 制限**: 公開 API のため認証不要ですが、レート制限対策として各リクエスト間に 0.5〜1 秒のスリープを入れています
- **Qiita の API 制限**: `QIITA_TOKEN` 環境変数が設定されていれば 1000 req/hour で動作します。未設定時は 60 req/hour（12クエリ × 1回/時間）。セットアップ手順は上記「初回セットアップ」を参照
- **Qiita レートリミット時の挙動**: 連続 403 が 3 回続くと自動で早期終了し、それまでの結果を保存します。`echo $QIITA_TOKEN` でトークンが設定されているか確認してください
