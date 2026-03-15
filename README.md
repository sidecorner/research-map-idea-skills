# research-map-idea-skills

アプリ・Webサービスの**穴場アイデアを調査・発掘するためのローカルスキル**プロジェクトです。

Reddit のペインポイント・Hacker News の注目投稿・Qiita の日本語開発者記事を自動収集し、Claude がアイデアを分析・スコアリングしてレポートとして出力します。

---

## 収録スキル

**すれ違い通信 × 手軽な情報交換アイデア調査**

Bluetooth・NFC・GPS を使った近接ソーシャル・出会い系コンテンツと、匿名・使い捨て・低摩擦な情報共有アプリの両軸で調査します。両テーマを組み合わせたアイデア（例:「その場を通った人に匿名のメモを残せる」）も対応します。

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

> このスキルは **このディレクトリ内でのみ** 有効です（`CLAUDE.md` によるローカルスキル登録）。

---

## ディレクトリ構成

```
research-map-idea-skills/
│
├── CLAUDE.md                    # ローカルスキル登録・プロジェクト設定
├── SKILL.md                     # スキル定義（すれ違い通信 × 軽量情報交換）
├── README.md                    # このファイル
│
├── scripts/
│   ├── fetch_reddit.py          # Reddit データ収集（40サブレディット）
│   ├── fetch_hn.py              # HN データ収集（53クエリ、--rolling 対応）
│   └── fetch_qiita.py           # Qiita データ収集（24クエリ、--rolling 対応）
│
├── references/
│   ├── analysis_guide.md        # データ分析・クロスリファレンスガイド
│   ├── idea_patterns.md         # アイデアパターン・制約適用ガイド
│   ├── scoring_rubric.md        # 5軸スコアリング基準
│   └── report_template.md       # レポートテンプレート
│
└── reports/
    └── {year}/
        └── yyyymmdd/            # ダッシュなし（例: 20260315）
            └── 214710.md        # 時刻hhmmss（24時間・セパレータなし）
```

---

## スキルの動作フロー

```
① 年号 + 条件確認（日本語で質問）
   → 今年指定 or 無指定: 直近1年間（ローリングウィンドウ）を使用
   → 過去年指定: その年の 01-01〜12-31 を使用
        ↓
② Reddit データ収集
   fetch_reddit.py --year {year}（40サブレディット）
        ↓
③ Hacker News データ収集
   fetch_hn.py --rolling（今年）/ --year {year}（過去年）（53クエリ・min-points 5）
   → 10件未満の場合は前年データを補完
        ↓
④ Qiita データ収集
   fetch_qiita.py --rolling（今年）/ --year {year}（過去年）（24クエリ）
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
   reports/{year}/{yyyymmdd}/{HHMMSS}.md
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

主なカバー領域（fetch_reddit.py・40サブレディット）:

| カテゴリ | サブレディット |
|---------|-------------|
| 位置情報ゲーム | r/pokemongo, r/Ingress, r/NianticWayfarer, r/streetpass |
| BLE / NFC / IoT | r/bluetooth, r/NFC, r/IoT, r/embedded |
| ハイパーローカル | r/Nextdoor, r/digitalnomad |
| プライバシー | r/privacy, r/privacytoolsIO |
| ウェアラブル | r/wearables, r/smartwatch |
| カジュアル Q&A | r/AskReddit, r/NoStupidQuestions, r/tipofmytongue, r/explainlikeimfive |
| 匿名表現 | r/confession, r/offmychest, r/TrueOffMyChest |
| デジタルミニマリズム | r/nosurf, r/digitalminimalism, r/CasualConversation |
| 生産性・ノートツール | r/productivity, r/Notion, r/ObsidianMD |
| インディー開発 | r/SideProject, r/indiehackers, r/AppIdeas, r/startups, r/Entrepreneur |
| アプリ全般 | r/androidapps, r/iosapps |
| コミュニティQ&A参照 | r/personalfinance, r/legaladvice |

---

## セットアップ（初回のみ）

### Qiita アクセストークンの設定

Qiita の検索にはトークンを推奨します（レート制限 60→1000 req/時）。

**1. トークンを発行する**
Qiita アカウントにログイン → 設定 → アプリケーション → 個人用アクセストークン
- スコープ: `read_qiita` のみにチェック
- トークン名: 任意（例: `research-map-idea-skills`）

**2. トークンファイルに保存する（推奨・Claude Code でも自動適用）**
```bash
mkdir -p ~/.config/qiita
echo "your_token_here" > ~/.config/qiita/token
chmod 600 ~/.config/qiita/token
```

**優先順位（3通りの指定方法）**

| 優先度 | 方法 | 用途 |
|--------|------|------|
| 1 | `--token YOUR_TOKEN` | 一時的な上書き |
| 2 | `export QIITA_TOKEN=xxx` in `~/.zshrc` | 端末での手動実行 |
| 3 | `~/.config/qiita/token` ファイル | **Claude Code 経由での自動実行（推奨）** |

> ⚠ トークンをこのプロジェクトのファイルには絶対に書かないでください。

---

## スクリプトの直接実行

Claude を介さず手動でデータ収集したい場合：

```bash
# Reddit（常に --year を使用、--rolling フラグは不要）
python scripts/fetch_reddit.py --year 2026 --limit 30 --output /tmp/reddit_2026.json

# Hacker News（直近1年ローリング）
python scripts/fetch_hn.py --rolling --min-points 5 --output /tmp/hn_rolling.json

# Hacker News（過去年）
python scripts/fetch_hn.py --year 2025 --min-points 5 --output /tmp/hn_2025.json

# Qiita（直近1年ローリング）※ QIITA_TOKEN 自動適用
python scripts/fetch_qiita.py --rolling --output /tmp/qiita_rolling.json

# Qiita（過去年）
python scripts/fetch_qiita.py --year 2025 --output /tmp/qiita_2025.json

# カスタム指定の例
python scripts/fetch_reddit.py --year 2026 --subreddits "AskReddit,SideProject,AppIdeas"
python scripts/fetch_hn.py --rolling --queries "ephemeral messaging,anonymous notes app"
python scripts/fetch_qiita.py --rolling --queries "すれ違い通信,BLE 近接,NFC"
```

Reddit / HN は認証不要（公開 API）。Qiita は認証なしで 60 req/hour、トークンあり（無料）で 1000 req/hour。

---

## レポート出力先

```
reports/
└── 2026/
    └── 20260315/
        └── 140000.md   ← 2026-03-15 14:00:00 に生成されたレポート
```

同一日に複数回実行すると、時刻の異なるファイルが追記されていきます。

---

## 注意事項

- **ローカル限定**: このスキルは `CLAUDE.md` によりこのディレクトリ内でのみ有効です
- **調査期間の自動決定**: 今年を指定した場合は直近1年間（ローリング）を使用。前年以前を指定した場合はその年の通年を使用します
- **当年の Reddit データ**: `--year 2026` のように当年を指定すると、Reddit API の `t=year`（過去12ヶ月ローリング）が自動で使われます
- **当年の HN データ**: 年初に実行すると投稿数が10件を下回る場合があります。スキルは自動で前年データを補完します
- **Qiita レートリミット時の挙動**: 連続 403 が 3 回続くと自動で早期終了し、それまでの結果を保存します
