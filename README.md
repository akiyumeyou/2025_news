# AI最新情報キャッチアップシステム

生成AI分野の最新情報を自動収集・分析し、週次ニュースレターを生成するシステムです。

## 機能

- **情報収集**: RSSフィード、API、Webスクレイピングによる自動情報収集
- **分類・分析**: 生成AI特化カテゴリ（バイブコーディング、コンテンツ生成、LLM、ビジネスAI等）への自動分類
- **重要度評価**: 生成AI研究者向けの重要度と注目度の分析
- **レポート生成**: 週次ニュースレターの自動生成（月曜夜発行）

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

# クイックテスト（5件制限）
python quick_test.py

# スケジューラーモード
python main.py --mode scheduler
```

## 🔑 APIキーについて

### 必要なAPIキー
- **NewsAPI** (オプション): https://newsapi.org/ で無料アカウント作成
- **OpenAI API** (オプション): より高度な分析に使用

### 無料で利用可能な機能
- **RSSフィード**: APIキー不要
- **Webスクレイピング**: APIキー不要
- **GitHub Trending**: APIキー不要
- **arXiv**: APIキー不要

### 制限事項
- `.env`ファイルはGitHubにアップロードされません（セキュリティのため）
- 初回利用時は手動でAPIキーを設定する必要があります
- 無料APIには利用制限があります（NewsAPI: 1000リクエスト/日）

## ディレクトリ構造

```
news/
├── main.py                 # メイン実行ファイル
├── quick_test.py          # クイックテスト用
├── test_system.py         # システムテスト用
├── config/
│   ├── sources.py         # 情報源設定（生成AI特化）
│   └── categories.py      # カテゴリ定義（生成AI特化）
├── modules/
│   ├── collector.py       # 情報収集モジュール
│   ├── analyzer.py        # 分析モジュール
│   ├── reporter.py        # レポート生成モジュール
│   └── scheduler.py       # スケジューリングモジュール
├── templates/
│   └── newsletter.html    # ニュースレターテンプレート
├── data/
│   └── collected/         # 収集データ保存
├── reports/
│   └── newsletters/       # 生成レポート保存
├── requirements.txt       # Python依存関係
├── .gitignore            # Git除外設定
└── env_example.txt       # 環境変数設定例
```

## 主なカテゴリ

- **💻 AI開発・プログラミング**: GitHub Copilot、バイブコーディング、コード生成
- **🎨 生成AI・コンテンツ生成**: DALL-E、Midjourney、Sora、画像・動画生成
- **🤖 大規模言語モデル・チャットボット**: ChatGPT、Claude、Gemini
- **🏢 ビジネス・企業AI**: 企業のAI導入、業務自動化
- **🔧 AIハードウェア・チップ**: GPU、TPU、AI専用チップ
- **⚖️ AI規制・倫理・安全性**: AI規制、倫理問題、安全性
- **💰 AIスタートアップ・資金調達**: AI関連の投資、資金調達 

## **即座にアクセス可能な方法**

### **方法1: 直接URLアクセス**
```
https://raw.githubusercontent.com/akiyumeyou/2025_news/main/index.html
```

### **方法2: GitHub上でHTML表示**
1. GitHubリポジトリページで `index.html` をクリック
2. **Raw** ボタンをクリック
3. ブラウザでHTMLが表示される

### **方法3: 手動でGitHub Pages設定**
1. https://github.com/akiyumeyou/2025_news/settings/pages にアクセス
2. **Source** で **Deploy from a branch** を選択
3. **Branch** で **main** を選択
4. **Folder** で **/ (root)** を選択
5. **Save** をクリック

## **申し訳ありません**

確かに私の手順に問題がありました。GitHub Pagesの設定は複雑で、自動化よりも手動設定の方が確実です。上記の方法3で手動設定していただければ、すぐにアクセス可能になります。 