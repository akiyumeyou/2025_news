# AI最新情報キャッチアップシステム

AI分野の最新情報を自動収集・分析し、週次ニュースレターを生成するシステムです。

## 機能

- **情報収集**: RSSフィード、NewsAPI、Webスクレイピングによる自動情報収集
- **カテゴリ分類**: 8つの専門カテゴリ（プログラミングツール、デザインAI、LLM、ハードウェア等）への自動分類
- **重要度評価**: 重要度と注目度による記事スコアリング
- **レポート生成**: HTMLとテキスト形式のニュースレター自動生成

## セットアップ

1. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

2. 環境変数の設定:
```bash
cp env_example.txt .env
# .envファイルを編集してAPIキーなどを設定
```

3. システムの実行:
```bash
# 手動実行
python main.py

# スケジューラーモード
python main.py --mode scheduler
```

## 🔑 APIキーについて

### 推奨APIキー
- **NewsAPI**: https://newsapi.org/ で無料アカウント作成（1000リクエスト/日）

### 無料で利用可能な機能
- **RSSフィード**: 主要AI企業ブログ（OpenAI、Google、Meta等）
- **Webスクレイピング**: Hacker News、Reddit AI関連
- **arXiv**: AI研究論文（現在無効化中）

### 制限事項
- NewsAPIキーは.envファイルで設定が必要
- 翻訳・サマリー機能は削除済み（シンプル化のため）

## ディレクトリ構造

```
news/
├── main.py                 # メイン実行ファイル
├── config/
│   ├── sources.py         # 情報源設定
│   └── categories.py      # カテゴリ定義（8つの専門分野）
├── modules/
│   ├── collector.py       # 情報収集モジュール
│   ├── analyzer.py        # 分析モジュール（簡素化済み）
│   ├── reporter.py        # レポート生成モジュール
│   └── scheduler.py       # スケジューリングモジュール
├── templates/
│   └── newsletter.html    # ニュースレターテンプレート
├── data/
│   └── collected/         # 収集データ保存
├── reports/
│   └── newsletters/       # 生成レポート保存
├── requirements.txt       # Python依存関係（8パッケージ）
└── .env                   # 環境変数設定（要手動作成）
```

## 8つの専門カテゴリ

1. **🚀 AI技術ブレークスルー**: 革新的なAI技術、研究成果、新手法
2. **🤖 主要LLMアップデート**: ChatGPT、Claude、Geminiなどの言語モデル
3. **🎨 デザイン・UI/UX AI**: エンジニア向けUI/UXデザイン支援、プロトタイピング
4. **🖼️ 画像・動画生成AI**: DALL-E、Midjourney、Sora、クリエイティブAI
5. **💻 プログラミングツール・開発環境**: IDE、フレームワーク、ライブラリの更新
6. **🤖 AIコーディング・開発支援**: AI搭載のコード生成、プログラミング支援
7. **🔧 AIハードウェア・チップ**: GPU、TPU、AI専用チップ
8. **📊 AI業界トレンド・総括**: 市場分析、将来予測、業界レポート

## 出力形式

- **HTMLレポート**: `reports/newsletters/newsletter_YYYYMMDD_HHMMSS.html`
- **テキストレポート**: `reports/newsletters/newsletter_YYYYMMDD_HHMMSS.txt`
- **収集データ**: `data/collected/articles_YYYYMMDD_HHMMSS.json`

## 特徴

- **重複除去**: カテゴリ別にタイトルベースで重複記事を自動除去
- **トップ10表示**: 各カテゴリで重要度・注目度が高い記事を10件まで表示
- **90件収集**: RSS、NewsAPI、スクレイピングで週に約90件の記事を収集
- **シンプル設計**: 翻訳・サマリー機能を削除し、必要最小限の機能に特化 