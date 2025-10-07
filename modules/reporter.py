"""
レポート生成モジュール
分析結果から週次ニュースレターを生成
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
from jinja2 import Template
import pandas as pd

logger = logging.getLogger(__name__)

class NewsletterReporter:
    def __init__(self):
        self.template_dir = "templates"
        self.reports_dir = "reports/newsletters"
        
        # ディレクトリ作成
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_newsletter(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """週次ニュースレターを生成"""
        logger.info("ニュースレター生成開始")
        
        articles = analysis_results['articles']
        summary = analysis_results['summary']
        
        # カテゴリ別記事の整理
        categorized_articles = self._organize_by_category(articles)
        
        # 重要記事の抽出
        important_articles = self._extract_important_articles(articles)
        
        # トレンド分析
        trends = self._analyze_trends(articles)
        
        # ニュースレターコンテンツ作成
        newsletter_content = self._create_newsletter_content(
            summary, categorized_articles, important_articles, trends
        )
        
        # HTMLレポート生成
        html_report = self._generate_html_report(newsletter_content)
        
        # テキストレポート生成
        text_report = self._generate_text_report(newsletter_content)
        
        # レポート保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self._save_reports(html_report, text_report, timestamp)
        
        return {
            'html_content': html_report,
            'text_content': text_report,
            'timestamp': timestamp,
            'summary': summary
        }
    
    def _organize_by_category(self, articles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """記事をカテゴリ別に整理（網羅的に表示、重複除去、トップ10表示）"""
        from config.categories import CATEGORIES
        
        # 全カテゴリを初期化
        categorized = {}
        for category_id in CATEGORIES.keys():
            categorized[category_id] = []
        
        # 一般カテゴリは削除（すべて特定カテゴリに分類するため）
        # categorized['general'] = []
        
        for article in articles:
            category = article.get('category', 'llm_chatbot')  # デフォルトはLLMカテゴリ
            
            # 重要度と注目度でソート用スコア
            article['combined_score'] = (
                article.get('importance_score', 0) + 
                article.get('attention_score', 0)
            )
            
            # カテゴリが存在する場合のみ追加
            if category in categorized:
                categorized[category].append(article)
        
        # 各カテゴリ内で重複除去とソート
        for category in categorized:
            # タイトルベースで重複除去
            unique_articles = self._remove_duplicates_by_title(categorized[category])
            
            # スコア順にソートしてトップ10を取得
            unique_articles.sort(
                key=lambda x: x['combined_score'], 
                reverse=True
            )
            categorized[category] = unique_articles[:10]  # トップ10に制限
        
        return categorized
    
    def _remove_duplicates_by_title(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """タイトルベースで重複記事を除去"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title = article.get('title', '')
            if not title:  # タイトルがNoneまたは空の場合はスキップ
                continue
                
            title_lower = title.lower().strip()
            # タイトルの一部が重複している場合も検出
            is_duplicate = False
            for seen_title in seen_titles:
                if (title_lower in seen_title or seen_title in title_lower) and len(title_lower) > 10:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_titles.add(title_lower)
                unique_articles.append(article)
        
        return unique_articles
    
    def _extract_important_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """重要記事を抽出（重要度・注目度が高いもの）"""
        important_articles = [
            article for article in articles
            if (article.get('importance_level') == 'high' or 
                article.get('attention_level') == 'high')
        ]
        
        # スコア順にソート
        important_articles.sort(
            key=lambda x: (x.get('importance_score', 0) + x.get('attention_score', 0)),
            reverse=True
        )
        
        return important_articles[:15]  # 上位15件
    
    def _analyze_trends(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """トレンド分析"""
        trends = {
            'top_categories': [],
            'emerging_topics': [],
            'key_companies': [],
            'technology_focus': []
        }
        
        # カテゴリ別記事数
        category_counts = {}
        for article in articles:
            category = article.get('category', 'general')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # 上位カテゴリ
        trends['top_categories'] = sorted(
            category_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        
        # キーワード分析
        all_titles = ' '.join([a.get('title', '') for a in articles])
        trends['emerging_topics'] = self._extract_emerging_topics(all_titles)
        
        return trends
    
    def _extract_emerging_topics(self, text: str) -> List[str]:
        """新興トピックを抽出"""
        # 簡単なキーワード分析（実際の実装ではより高度な分析が必要）
        keywords = [
            'AI', 'machine learning', 'deep learning', 'generative',
            'automation', 'robotics', 'autonomous', 'intelligent',
            'neural', 'algorithm', 'model', 'framework'
        ]
        
        emerging = []
        text_lower = text.lower()
        
        for keyword in keywords:
            if keyword.lower() in text_lower:
                emerging.append(keyword)
        
        return emerging[:5]  # 上位5件
    
    def _create_newsletter_content(self, summary: Dict[str, Any], 
                                 categorized_articles: Dict[str, List[Dict[str, Any]]],
                                 important_articles: List[Dict[str, Any]],
                                 trends: Dict[str, Any]) -> Dict[str, Any]:
        """ニュースレターコンテンツを作成"""
        
        # 週次サマリー
        week_summary = {
            'total_articles': summary['total_articles'],
            'high_importance_count': summary['importance_levels'].get('high', 0),
            'high_attention_count': summary['attention_levels'].get('high', 0),
            'date_range': self._get_date_range(),
            'generated_date': datetime.now().strftime('%Y年%m月%d日'),
            'ai_summary': self._generate_week_summary(summary, important_articles)
        }
        
        # カテゴリ別サマリー（全カテゴリを表示、空のカテゴリも含む）
        from config.categories import CATEGORIES
        category_summary = []
        
        for category_id, category_config in CATEGORIES.items():
            category_info = summary['categories'].get(category_id, {
                'name': category_config['name'],
                'count': 0,
                'high_importance': 0,
                'high_attention': 0
            })
            
            category_summary.append({
                'id': category_id,
                'name': category_info['name'],
                'count': category_info['count'],
                'high_importance': category_info['high_importance'],
                'high_attention': category_info['high_attention'],
                'description': category_config['description']
            })
        
        # 一般カテゴリは削除（すべて特定カテゴリに分類されるため）
        
        return {
            'week_summary': week_summary,
            'category_summary': category_summary,
            'categorized_articles': categorized_articles,
            'important_articles': important_articles,
            'trends': trends,
            'top_articles': summary['top_articles']
        }
    
    def _get_date_range(self) -> str:
        """日付範囲を取得"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        return f"{start_date.strftime('%m月%d日')} - {end_date.strftime('%m月%d日')}"
    
    def _generate_html_report(self, content: Dict[str, Any]) -> str:
        """HTMLレポートを生成"""
        template = self._load_html_template()
        
        # テンプレート変数
        template_vars = {
            'week_summary': content['week_summary'],
            'category_summary': content['category_summary'],
            'categorized_articles': content['categorized_articles'],  # 元のデータを使用
            'important_articles': content['important_articles'],  # 元のデータを使用
            'trends': content['trends'],
            'top_articles': content['top_articles']
        }
        
        # デバッグ用：top_articlesの内容を確認
        logger.info(f"top_articles type: {type(content['top_articles'])}")
        if content['top_articles']:
            logger.info(f"top_articles[0] type: {type(content['top_articles'][0])}")
            logger.info(f"top_articles[0] keys: {content['top_articles'][0].keys() if isinstance(content['top_articles'][0], dict) else 'Not a dict'}")
        
        return template.render(**template_vars)
    
    def _load_html_template(self) -> Template:
        """HTMLテンプレートを読み込み"""
        template_path = os.path.join(self.template_dir, "newsletter.html")
        
        if not os.path.exists(template_path):
            # デフォルトテンプレートを作成
            self._create_default_template()
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        return Template(template_content)
    
    def _create_default_template(self):
        """デフォルトHTMLテンプレートを作成"""
        template_content = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI最新情報ニュースレター</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; line-height: 1.6; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; border-bottom: 3px solid #007acc; padding-bottom: 20px; margin-bottom: 30px; }
        .header h1 { color: #007acc; margin: 0; font-size: 2.2em; }
        .summary { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px; border-left: 4px solid #007acc; }
        .category { margin-bottom: 40px; }
        .category h2 { color: #333; border-left: 4px solid #007acc; padding-left: 15px; margin-bottom: 20px; }
        .featured-article { margin-bottom: 25px; padding: 20px; border: 2px solid #007acc; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,123,204,0.1); }
        .featured-article h3 { margin: 0 0 15px 0; color: #007acc; font-size: 1.4em; }
        .featured-article .description { margin: 15px 0; color: #333; font-size: 1.1em; line-height: 1.6; }
        .featured-article .meta { font-size: 0.9em; color: #666; margin-top: 15px; padding-top: 10px; border-top: 1px solid #eee; }
        .link-only { margin: 8px 0; padding: 10px 15px; background: #f8f9fa; border-left: 3px solid #007acc; border-radius: 4px; }
        .link-only a { color: #007acc; text-decoration: none; font-weight: 500; }
        .link-only a:hover { text-decoration: underline; }
        .link-only .source { font-size: 0.85em; color: #666; margin-left: 10px; }
        .scores { font-size: 0.9em; color: #888; }
        .featured-badge { background: #dc3545; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8em; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI最新情報ニュースレター</h1>
            <p>{{ week_summary.generated_date }} | {{ week_summary.date_range }}</p>
        </div>
        
        <div class="summary">
            <h2>📊 今週のサマリー</h2>
            <p><strong>総記事数:</strong> {{ week_summary.total_articles }}件</p>
            <p><strong>高重要度記事:</strong> {{ week_summary.high_importance_count }}件</p>
            <p><strong>高注目度記事:</strong> {{ week_summary.high_attention_count }}件</p>
        </div>
        
        <div class="category">
            <h2>🔥 注目記事トップ3（詳細版）</h2>
            {% for article in top_articles[:3] %}
            <div class="featured-article">
                <div class="featured-badge">TOP {{ loop.index }}</div>
                <h3><a href="{{ article.link }}" target="_blank">{{ article.title }}</a></h3>
                <div class="description">
                    {{ article.description if article.description else 'AI関連の重要なニュースです。詳細は記事をご確認ください。' }}
                </div>
                <div class="meta">
                    <strong>カテゴリ:</strong> {{ article.category }} | <strong>ソース:</strong> {{ article.source }}<br>
                    <span class="scores">重要度スコア: {{ "%.2f"|format(article.importance_score) }} | 注目度スコア: {{ "%.2f"|format(article.attention_score) }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div class="category">
            <h2>📋 その他の注目記事（タイトル＆リンク）</h2>
            {% for article in top_articles[3:] %}
            <div class="link-only">
                <a href="{{ article.link }}" target="_blank">{{ article.title }}</a>
                <span class="source">[{{ article.source }}]</span>
            </div>
            {% endfor %}
        </div>
        
        <div class="category">
            <h2>📂 カテゴリ別記事リスト</h2>
            {% for category_id, articles in categorized_articles.items() %}
            {% if articles %}
            <h3>{{ category_id.replace('_', ' ').title() }}</h3>
            {% for article in articles[:10] %}
            <div class="link-only">
                <a href="{{ article.link }}" target="_blank">{{ article.title }}</a>
                <span class="source">[{{ article.source }}]</span>
            </div>
            {% endfor %}
            {% endif %}
            {% endfor %}
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: #e3f2fd; border-radius: 8px; text-align: center;">
            <p><small>🤖 このニュースレターは自動生成されました | 生成日時: {{ week_summary.generated_date }}</small></p>
        </div>
    </div>
</body>
</html>
        """
        
        os.makedirs(self.template_dir, exist_ok=True)
        with open(os.path.join(self.template_dir, "newsletter.html"), 'w', encoding='utf-8') as f:
            f.write(template_content)
    
    def _generate_category_html(self, categorized_articles: Dict[str, List[Dict[str, Any]]]) -> Dict[str, str]:
        """カテゴリ別記事のHTMLを生成"""
        category_html = {}
        
        for category_id, articles in categorized_articles.items():
            html_parts = []
            for article in articles[:10]:  # 各カテゴリ上位10件
                description = article.get('description', '')
                if isinstance(description, str):
                    description = description[:200] + "..." if len(description) > 200 else description
                else:
                    description = ""
                
                html_parts.append(f"""
                <div class="article {article.get('importance_level', 'low')}">
                    <h3><a href="{article.get('link', '#')}" target="_blank">{article.get('title', '')}</a></h3>
                    <p>{description}</p>
                    <p>ソース: {article.get('source', '')} | 重要度: {article.get('importance_level', 'low')} | 注目度: {article.get('attention_level', 'low')}</p>
                </div>
                """)
            
            category_html[category_id] = '\n'.join(html_parts)
        
        return category_html
    
    def _generate_important_articles_html(self, important_articles: List[Dict[str, Any]]) -> str:
        """重要記事のHTMLを生成"""
        html_parts = []
        
        for article in important_articles:
            description = article.get('description', '')
            if isinstance(description, str):
                description = description[:200] + "..." if len(description) > 200 else description
            else:
                description = ""
            
            html_parts.append(f"""
            <div class="article important">
                <h3><a href="{article.get('link', '#')}" target="_blank">{article.get('title', '')}</a></h3>
                <p>{description}</p>
                <p>カテゴリ: {article.get('category_name', '')} | ソース: {article.get('source', '')}</p>
                <p class="scores">重要度: {article.get('importance_score', 0):.2f} | 注目度: {article.get('attention_score', 0):.2f}</p>
            </div>
            """)
        
        return '\n'.join(html_parts)
    
    def _generate_text_report(self, content: Dict[str, Any]) -> str:
        """テキストレポートを生成"""
        text_parts = []
        
        # ヘッダー
        text_parts.append("=" * 60)
        text_parts.append("🤖 AI最新情報ニュースレター")
        text_parts.append(f"発行日: {content['week_summary']['generated_date']}")
        text_parts.append(f"対象期間: {content['week_summary']['date_range']}")
        text_parts.append("=" * 60)
        text_parts.append("")
        
        # サマリー
        text_parts.append("📊【今週のサマリー】")
        text_parts.append(f"総記事数: {content['week_summary']['total_articles']}件")
        text_parts.append(f"高重要度記事: {content['week_summary']['high_importance_count']}件")
        text_parts.append(f"高注目度記事: {content['week_summary']['high_attention_count']}件")
        text_parts.append("")
        
        # トップ3記事（詳細版）
        text_parts.append("🔥【注目記事トップ3（詳細版）】")
        for i, article in enumerate(content['top_articles'][:3], 1):
            text_parts.append(f"■ TOP {i}: {article['title']}")
            text_parts.append(f"   📖 内容: {article.get('description', 'AI関連の重要なニュースです。詳細は記事をご確認ください。')}")
            text_parts.append(f"   🏷️  カテゴリ: {article['category']} | ソース: {article['source']}")
            text_parts.append(f"   📊 重要度: {article['importance_score']:.2f} | 注目度: {article['attention_score']:.2f}")
            text_parts.append(f"   🔗 リンク: {article['link']}")
            text_parts.append("")
        
        # その他の注目記事（タイトル&リンクのみ）
        if len(content['top_articles']) > 3:
            text_parts.append("📋【その他の注目記事（タイトル&リンク）】")
            for i, article in enumerate(content['top_articles'][3:], 4):
                text_parts.append(f"{i}. {article['title']} [{article['source']}]")
                text_parts.append(f"   🔗 {article['link']}")
        
        text_parts.append("")
        
        # カテゴリ別記事（タイトル&リンクのみ）
        text_parts.append("📂【カテゴリ別記事リスト】")
        for category_id, articles in content['categorized_articles'].items():
            if articles:
                text_parts.append(f"\n■ {category_id.replace('_', ' ').upper()}")
                for i, article in enumerate(articles[:10], 1):
                    text_parts.append(f"  {i}. {article['title']} [{article['source']}]")
                    text_parts.append(f"     🔗 {article['link']}")
        
        text_parts.append("")
        text_parts.append("=" * 60)
        text_parts.append(f"🤖 自動生成レポート | 生成日時: {content['week_summary']['generated_date']}")
        text_parts.append("=" * 60)
        
        return '\n'.join(text_parts)
    
    def _save_reports(self, html_content: str, text_content: str, timestamp: str):
        """レポートを保存"""
        # HTMLレポート保存
        html_filename = os.path.join(self.reports_dir, f"newsletter_{timestamp}.html")
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # テキストレポート保存
        text_filename = os.path.join(self.reports_dir, f"newsletter_{timestamp}.txt")
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        # index.htmlを更新
        self._update_index_html()
        
        logger.info(f"レポート保存完了: {html_filename}, {text_filename}")
    
    def _update_index_html(self):
        """index.htmlを最新の3つのニュースレターで更新"""
        try:
            # reportsディレクトリから最新のニュースレターを取得
            newsletter_files = []
            for filename in os.listdir(self.reports_dir):
                if filename.startswith('newsletter_') and filename.endswith('.html'):
                    # タイムスタンプを抽出
                    timestamp = filename.replace('newsletter_', '').replace('.html', '')
                    newsletter_files.append((timestamp, filename))
            
            # タイムスタンプ順にソート（新しい順）
            newsletter_files.sort(reverse=True)
            latest_newsletters = newsletter_files[:3]
            
            # index.htmlの内容を生成
            index_content = self._generate_index_html(latest_newsletters)
            
            # index.htmlを保存
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            logger.info(f"index.html更新完了: 最新{len(latest_newsletters)}件のニュースレターを表示")
            
        except Exception as e:
            logger.error(f"index.html更新エラー: {e}")
    
    def _generate_index_html(self, newsletters: list) -> str:
        """index.htmlの内容を生成"""
        html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI最新情報ニュースレター一覧</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background-color: #f5f5f5; 
            line-height: 1.6;
        }
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
        }
        .header { 
            text-align: center; 
            border-bottom: 3px solid #007acc; 
            padding-bottom: 20px; 
            margin-bottom: 30px; 
        }
        .header h1 { 
            color: #007acc; 
            margin: 0; 
            font-size: 2.5em;
        }
        .newsletter-item { 
            margin-bottom: 25px; 
            padding: 25px; 
            border: 2px solid #e9ecef; 
            border-radius: 10px; 
            background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
            transition: all 0.3s ease;
        }
        .newsletter-item:hover { 
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-color: #007acc; 
            box-shadow: 0 4px 15px rgba(0,123,204,0.2);
        }
        .newsletter-item.latest {
            border-color: #007acc;
            border-width: 3px;
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        }
        .newsletter-item h3 { 
            margin: 0 0 15px 0; 
            color: #007acc; 
            font-size: 1.4em;
        }
        .newsletter-item a { 
            color: #007acc; 
            text-decoration: none; 
            font-weight: 600;
        }
        .newsletter-item a:hover { 
            text-decoration: underline; 
        }
        .meta { 
            font-size: 0.95em; 
            color: #666; 
            margin-top: 15px; 
            padding-top: 15px;
            border-top: 1px solid #ddd;
        }
        .badge { 
            display: inline-block; 
            padding: 6px 12px; 
            border-radius: 20px; 
            font-size: 0.85em; 
            font-weight: 600;
            margin-right: 10px; 
            text-decoration: none !important;
        }
        .badge-html { 
            background: #28a745; 
            color: white; 
        }
        .badge-txt { 
            background: #007acc; 
            color: white; 
        }
        .latest-badge {
            background: #dc3545;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            display: inline-block;
            margin-left: 10px;
        }
        .system-info {
            margin-top: 40px; 
            padding: 25px; 
            background: linear-gradient(135deg, #e8f5e8 0%, #f0f8ff 100%);
            border-radius: 10px;
            border-left: 4px solid #007acc;
        }
        .system-info h3 {
            color: #007acc;
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI最新情報ニュースレター一覧</h1>
            <p>生成AI分野の最新情報を自動収集・分析した週次ニュースレター</p>
        </div>
        
"""
        
        # ニュースレター項目を生成
        for i, (timestamp, filename) in enumerate(newsletters):
            # タイムスタンプから日付を生成
            try:
                date_str = f"{timestamp[:4]}年{timestamp[4:6]}月{timestamp[6:8]}日"
            except:
                date_str = timestamp
            
            is_latest = i == 0
            latest_class = " latest" if is_latest else ""
            latest_badge = '<span class="latest-badge">最新</span>' if is_latest else ""
            
            html_content += f"""        <div class="newsletter-item{latest_class}">
            <h3>
                <a href="reports/newsletters/{filename}" target="_blank">{date_str} ニュースレター</a>
                {latest_badge}
            </h3>
            <p>AI関連の最新ニュースを重要度順に整理。トップ3記事は詳細表示、その他はタイトル・リンク形式で掲載。</p>
            <div class="meta">
                <a href="reports/newsletters/{filename}" target="_blank" class="badge badge-html">📄 HTML版で読む</a>
                <a href="reports/newsletters/{filename.replace('.html', '.txt')}" target="_blank" class="badge badge-txt">📝 テキスト版</a>
            </div>
        </div>
        
"""
        
        html_content += """        <div class="system-info">
            <h3>📋 システム概要</h3>
            <ul>
                <li><strong>🔍 自動収集</strong>: RSS、NewsAPI、スクレイピングによる多角的なニュース収集</li>
                <li><strong>🏷️ AI分析</strong>: 重要度・注目度の自動評価とカテゴリ分類</li>
                <li><strong>📊 スマート表示</strong>: トップ3記事は詳細、その他はタイトル・リンクのみの効率的な情報提供</li>
                <li><strong>🔄 自動更新</strong>: 最新3件のニュースレターを自動表示</li>
                <li><strong>🛠️ 技術</strong>: Python、機械学習、自然言語処理を活用した高度な分析システム</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
        
        return html_content
    
    def _generate_week_summary(self, summary: Dict[str, Any], important_articles: List[Dict[str, Any]]) -> str:
        """今週のAIサマリーコメントを生成（簡易版）"""
        try:
            total_articles = summary['total_articles']
            high_importance = summary['importance_levels'].get('high', 0)
            
            # カテゴリ別の記事数を取得
            top_categories = []
            for category_id, category_info in summary['categories'].items():
                if category_info['count'] > 0:
                    top_categories.append((category_info['name'], category_info['count']))
            
            top_categories.sort(key=lambda x: x[1], reverse=True)
            
            # 重要な記事のタイトルを取得
            top_titles = [article.get('title', '')[:50] + '...' for article in important_articles[:3]]
            
            # サマリーテキストを生成
            summary_parts = []
            summary_parts.append(f"📊 今週は{total_articles}件のAI関連記事を収集しました。")
            
            if high_importance > 0:
                summary_parts.append(f"このうち{high_importance}件が高重要度記事として分類されています。")
            
            if top_categories:
                category_text = "、".join([f"{name}({count}件)" for name, count in top_categories[:3]])
                summary_parts.append(f"主要カテゴリは{category_text}です。")
            
            if top_titles:
                summary_parts.append("注目記事には以下が含まれます：")
                for i, title in enumerate(top_titles, 1):
                    summary_parts.append(f"{i}. {title}")
            
            summary_parts.append("🤖 各記事の詳細は下記をご覧ください。")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            logger.error(f"週次サマリー生成エラー: {e}")
            return "📊 今週のAI関連ニュースをまとめました。詳細は下記の記事一覧をご覧ください。" 