"""
情報収集モジュール
RSSフィード、API、Webスクレイピングによる情報収集
"""

import requests
import feedparser
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import json
import os
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

from config.sources import RSS_SOURCES, API_SOURCES, SCRAPING_SOURCES, ADDITIONAL_SOURCES, COLLECTION_CONFIG

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.collected_data = []
    
    def collect_rss_feeds(self) -> List[Dict[str, Any]]:
        """RSSフィードから情報を収集"""
        articles = []
        
        for source in RSS_SOURCES:
            try:
                logger.info(f"RSS収集開始: {source['name']}")
                feed = feedparser.parse(source['url'])
                
                for entry in feed.entries[:COLLECTION_CONFIG['max_articles_per_source']]:
                    # 日付フィルタリング
                    pub_date = self._parse_date(entry.get('published', ''))
                    if not self._is_recent(pub_date):
                        continue
                    
                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'description': entry.get('summary', ''),
                        'published_date': pub_date,
                        'source': source['name'],
                        'source_type': 'rss',
                        'category': source['category'],
                        'priority': source['priority']
                    }
                    
                    # 除外キーワードチェック
                    if not self._should_exclude(article['title']):
                        articles.append(article)
                
                time.sleep(1)  # レート制限対策
                
            except Exception as e:
                logger.error(f"RSS収集エラー {source['name']}: {e}")
        
        return articles
    
    def collect_api_news(self) -> List[Dict[str, Any]]:
        """APIからニュースを収集"""
        articles = []
        
        for source in API_SOURCES:
            try:
                api_key = os.getenv(source['api_key_env'])
                if not api_key:
                    logger.warning(f"APIキーが見つかりません: {source['api_key_env']}")
                    continue
                
                logger.info(f"API収集開始: {source['name']}")
                
                # 各キーワードで検索
                for keyword in source['keywords']:
                    params = source['params'].copy()
                    params['q'] = keyword
                    params['apiKey'] = api_key
                    
                    response = self.session.get(source['base_url'], params=params)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    for article_data in data.get('articles', [])[:5]:  # 明示的に5件制限
                        pub_date = self._parse_date(article_data.get('publishedAt', ''))
                        if not self._is_recent(pub_date):
                            continue
                        
                        article = {
                            'title': article_data.get('title', ''),
                            'link': article_data.get('url', ''),
                            'description': article_data.get('description', ''),
                            'published_date': pub_date,
                            'source': article_data.get('source', {}).get('name', source['name']),
                            'source_type': 'api',
                            'category': 'general',
                            'priority': 'medium',
                            'keyword': keyword
                        }
                        
                        if not self._should_exclude(article['title']):
                            articles.append(article)
                    
                    time.sleep(1)  # レート制限対策
                
            except Exception as e:
                logger.error(f"API収集エラー {source['name']}: {e}")
        
        return articles
    
    def collect_scraping_news(self) -> List[Dict[str, Any]]:
        """Webスクレイピングでニュースを収集"""
        articles = []
        
        for source in SCRAPING_SOURCES:
            try:
                logger.info(f"スクレイピング開始: {source['name']}")
                
                response = self.session.get(source['url'])
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                elements = soup.select(source['selector'])
                
                for element in elements[:COLLECTION_CONFIG['max_articles_per_source']]:
                    title_elem = element.select_one(source['title_selector'])
                    link_elem = element.select_one(source['link_selector'])
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        link = link_elem.get('href', '')
                        
                        # 相対URLを絶対URLに変換
                        if link.startswith('/'):
                            link = f"{source['url'].rstrip('/')}{link}"
                        
                        article = {
                            'title': title,
                            'link': link,
                            'description': '',
                            'published_date': datetime.now(),
                            'source': source['name'],
                            'source_type': 'scraping',
                            'category': source['category'],
                            'priority': source['priority']
                        }
                        
                        if not self._should_exclude(article['title']):
                            articles.append(article)
                
                time.sleep(2)  # スクレイピングの間隔
                
            except Exception as e:
                logger.error(f"スクレイピングエラー {source['name']}: {e}")
        
        return articles
    
    def collect_additional_sources(self) -> List[Dict[str, Any]]:
        """追加ソースから情報を収集"""
        articles = []
        
        try:
            # arXiv APIから論文情報を取得
            arxiv_source = ADDITIONAL_SOURCES['arxiv']
            logger.info(f"arXiv収集開始: {arxiv_source['name']}")
            
            response = self.session.get(arxiv_source['url'])
            response.raise_for_status()
            
            # XMLパース（簡易版）
            content = response.text
            import re
            
            # 論文タイトルを抽出
            titles = re.findall(r'<title>(.*?)</title>', content)
            links = re.findall(r'<id>(.*?)</id>', content)
            
            for i, (title, link) in enumerate(zip(titles[1:], links[:5])):  # 最初のタイトルは除外
                if 'AI' in title or 'artificial intelligence' in title.lower():
                    article = {
                        'title': title,
                        'link': link,
                        'description': f"arXiv論文: {title}",
                        'published_date': datetime.now(),
                        'source': arxiv_source['name'],
                        'source_type': 'arxiv',
                        'category': arxiv_source['category'],
                        'priority': arxiv_source['priority']
                    }
                    articles.append(article)
            
            logger.info(f"arXiv収集完了: {len(articles)}件")
            
        except Exception as e:
            logger.error(f"arXiv収集エラー: {e}")
        
        return articles
    
    def collect_all(self) -> List[Dict[str, Any]]:
        """全てのソースから情報を収集"""
        logger.info("情報収集開始")
        
        all_articles = []
        
        # RSS収集
        rss_articles = self.collect_rss_feeds()
        all_articles.extend(rss_articles)
        logger.info(f"RSS収集完了: {len(rss_articles)}件")
        
        # API収集
        api_articles = self.collect_api_news()
        all_articles.extend(api_articles)
        logger.info(f"API収集完了: {len(api_articles)}件")
        
        # スクレイピング収集
        scraping_articles = self.collect_scraping_news()
        all_articles.extend(scraping_articles)
        logger.info(f"スクレイピング収集完了: {len(scraping_articles)}件")
        
        # 追加ソース収集
        additional_articles = self.collect_additional_sources()
        all_articles.extend(additional_articles)
        logger.info(f"追加ソース収集完了: {len(additional_articles)}件")
        
        # 重複除去
        unique_articles = self._remove_duplicates(all_articles)
        logger.info(f"重複除去後: {len(unique_articles)}件")
        
        # データ保存
        self._save_collected_data(unique_articles)
        
        return unique_articles
    
    def _parse_date(self, date_str: str) -> datetime:
        """日付文字列をパース"""
        try:
            # 複数の日付形式に対応
            date_formats = [
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%dT%H:%M:%S%z',
                '%a, %d %b %Y %H:%M:%S %Z',
                '%a, %d %b %Y %H:%M:%S %z',
                '%Y-%m-%d %H:%M:%S'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # パースできない場合は現在時刻
            return datetime.now()
            
        except Exception:
            return datetime.now()
    
    def _is_recent(self, pub_date: datetime) -> bool:
        """最近の記事かどうかチェック"""
        if not pub_date:
            return False
        
        # タイムゾーン情報を統一
        now = datetime.now()
        if pub_date.tzinfo is None:
            pub_date = pub_date.replace(tzinfo=now.tzinfo)
        if now.tzinfo is None:
            now = now.replace(tzinfo=pub_date.tzinfo)
        
        min_date = now - timedelta(days=7)
        return pub_date >= min_date
    
    def _should_exclude(self, title: str) -> bool:
        """除外すべき記事かどうかチェック"""
        title_lower = title.lower()
        for keyword in COLLECTION_CONFIG['exclude_keywords']:
            if keyword.lower() in title_lower:
                return True
        return False
    
    def _remove_duplicates(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """重複記事を除去"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title_lower = article['title'].lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique_articles.append(article)
        
        return unique_articles
    
    def _save_collected_data(self, articles: List[Dict[str, Any]]):
        """収集データを保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data/collected/articles_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"データ保存完了: {filename}")
        
        # CSV形式でも保存
        df = pd.DataFrame(articles)
        csv_filename = f"data/collected/articles_{timestamp}.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        logger.info(f"CSV保存完了: {csv_filename}") 