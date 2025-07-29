"""
分析モジュール
収集した記事のカテゴリ分類と重要度評価
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
import logging
from datetime import datetime
import json
import os
import re

from config.categories import CATEGORIES, IMPORTANCE_CRITERIA

logger = logging.getLogger(__name__)

class NewsAnalyzer:
    def __init__(self):
        self.categories = CATEGORIES
        self.importance_criteria = IMPORTANCE_CRITERIA
        
        # 翻訳・サマリー機能は削除済み
    
    def analyze_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """記事の分析を実行"""
        logger.info("記事分析開始")
        
        # カテゴリ分類
        categorized_articles = self._categorize_articles(articles)
        
        # 重要度評価
        analyzed_articles = self._evaluate_importance(categorized_articles)
        
        # 注目度計算
        articles_with_attention = self._calculate_attention_score(analyzed_articles)
        
        # 翻訳・サマリー機能は削除（必要最小限の機能のみ）
        articles_with_enhancements = articles_with_attention
        
        # 分析結果の集計
        summary = self._create_analysis_summary(articles_with_enhancements)
        
        # 結果保存
        self._save_analysis_results(articles_with_enhancements, summary)
        
        return {
            'articles': articles_with_enhancements,
            'summary': summary
        }
    
    def _categorize_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """記事をカテゴリに分類"""
        categorized_articles = []
        
        for article in articles:
            title = article.get('title', '') or ''
            description = article.get('description', '') or ''
            content = f"{title.lower()} {description.lower()}"
            
            # 各カテゴリのキーワードとのマッチング
            best_category = None
            best_score = 0
            
            for category_id, category_info in self.categories.items():
                score = self._calculate_category_score(content, category_info['keywords'])
                
                if score > best_score:
                    best_score = score
                    best_category = category_id
            
            # スコアが閾値を超える場合のみカテゴリを設定（閾値を下げて分類精度向上）
            if best_score > 0.05:  # 5%以上のマッチング（より多くの記事を分類）
                article['category'] = best_category
                article['category_score'] = best_score
                article['category_name'] = self.categories[best_category]['name']
            else:
                # 一般カテゴリは削除し、最もスコアの高いカテゴリに分類
                if best_category:
                    article['category'] = best_category
                    article['category_score'] = best_score
                    article['category_name'] = self.categories[best_category]['name']
                else:
                    # どのカテゴリにもマッチしない場合のみ一般に分類
                    article['category'] = 'llm_chatbot'  # デフォルトでLLMカテゴリに
                    article['category_score'] = 0
                    article['category_name'] = self.categories['llm_chatbot']['name']
            
            categorized_articles.append(article)
        
        return categorized_articles
    
    def _calculate_category_score(self, content: str, keywords: List[str]) -> float:
        """カテゴリとのマッチングスコアを計算"""
        if not content or not keywords:
            return 0.0
        
        matches = 0
        total_keywords = len(keywords)
        
        for keyword in keywords:
            if keyword.lower() in content:
                matches += 1
        
        return matches / total_keywords if total_keywords > 0 else 0.0
    
    def _evaluate_importance(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """記事の重要度を評価"""
        evaluated_articles = []
        
        for article in articles:
            importance_score = self._calculate_importance_score(article)
            importance_level = self._determine_importance_level(importance_score)
            
            article['importance_score'] = importance_score
            article['importance_level'] = importance_level
            article['importance_description'] = self.importance_criteria[importance_level]['description']
            
            evaluated_articles.append(article)
        
        return evaluated_articles
    
    def _calculate_importance_score(self, article: Dict[str, Any]) -> float:
        """重要度スコアを計算"""
        score = 0.0
        
        # ソースの信頼性
        source_priority = article.get('priority', 'medium')
        if source_priority == 'high':
            score += 0.3
        elif source_priority == 'medium':
            score += 0.2
        else:
            score += 0.1
        
        # カテゴリスコア
        category_score = article.get('category_score', 0)
        score += category_score * 0.3
        
        # タイトルの重要キーワード
        title_importance = self._analyze_title_importance(article.get('title', ''))
        score += title_importance * 0.2
        
        # 内容の詳細度
        content_detail = self._analyze_content_detail(article.get('description', ''))
        score += content_detail * 0.2
        
        return min(score, 1.0)  # 最大1.0に制限
    
    def _analyze_title_importance(self, title: str) -> float:
        """タイトルの重要度を分析（生成AI特化）"""
        if not title:
            return 0.0
        
        # 生成AI関連の重要キーワード
        important_keywords = [
            'breakthrough', 'new', 'first', 'launch', 'release',
            'announcement', 'innovation', 'revolutionary', 'groundbreaking',
            'major', 'significant', 'important', 'key', 'critical',
            # 生成AI特化キーワード
            'GPT', 'DALL-E', 'Midjourney', 'Stable Diffusion', 'Sora',
            'Copilot', 'code generation', 'generative', 'diffusion',
            'transformer', 'LLM', 'large language model'
        ]
        
        title_lower = title.lower()
        matches = sum(1 for keyword in important_keywords if keyword.lower() in title_lower)
        
        return min(matches * 0.15, 1.0)  # 重みを調整
    
    def _analyze_content_detail(self, description: str) -> float:
        """内容の詳細度を分析"""
        if not description:
            return 0.0
        
        # 文字数による詳細度
        length_score = min(len(description) / 500, 1.0)
        
        # 技術的な詳細の有無
        technical_indicators = [
            'algorithm', 'model', 'architecture', 'framework',
            'performance', 'accuracy', 'benchmark', 'evaluation',
            'research', 'study', 'analysis', 'implementation'
        ]
        
        desc_lower = description.lower()
        technical_matches = sum(1 for indicator in technical_indicators if indicator in desc_lower)
        technical_score = min(technical_matches * 0.1, 0.5)
        
        return (length_score + technical_score) / 2
    
    def _determine_importance_level(self, score: float) -> str:
        """重要度レベルを決定"""
        if score >= 0.7:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_attention_score(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """注目度スコアを計算"""
        articles_with_attention = []
        
        for article in articles:
            attention_score = self._calculate_attention_metrics(article)
            article['attention_score'] = attention_score
            article['attention_level'] = self._determine_attention_level(attention_score)
            
            articles_with_attention.append(article)
        
        return articles_with_attention
    
    def _calculate_attention_metrics(self, article: Dict[str, Any]) -> float:
        """注目度メトリクスを計算"""
        score = 0.0
        
        # 重要度スコア
        importance_score = article.get('importance_score', 0)
        score += importance_score * 0.4
        
        # カテゴリスコア
        category_score = article.get('category_score', 0)
        score += category_score * 0.3
        
        # 時事性（新しい記事ほど高スコア）
        days_old = self._calculate_days_old(article.get('published_date'))
        recency_score = max(0, 1 - (days_old / 7))  # 1週間以内
        score += recency_score * 0.3
        
        return min(score, 1.0)
    
    def _calculate_days_old(self, pub_date) -> int:
        """記事の経過日数を計算"""
        if isinstance(pub_date, str):
            try:
                pub_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
            except:
                return 7  # パースできない場合は7日として扱う
        
        if not pub_date:
            return 7
        
        # タイムゾーン情報を統一
        now = datetime.now()
        if pub_date.tzinfo is not None:
            # pub_dateがタイムゾーン情報を持つ場合、nowもタイムゾーン対応にする
            import pytz
            now = now.replace(tzinfo=pytz.UTC)
        elif now.tzinfo is not None:
            # nowがタイムゾーン情報を持つ場合、pub_dateのタイムゾーン情報を削除
            pub_date = pub_date.replace(tzinfo=None)
        
        days_old = (now - pub_date).days
        return max(0, days_old)
    
    def _determine_attention_level(self, score: float) -> str:
        """注目度レベルを決定"""
        if score >= 0.7:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _create_analysis_summary(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析結果のサマリーを作成"""
        summary = {
            'total_articles': len(articles),
            'categories': {},
            'importance_levels': {},
            'attention_levels': {},
            'top_articles': [],
            'category_breakdown': {}
        }
        
        # カテゴリ別集計
        for category_id, category_info in self.categories.items():
            category_articles = [a for a in articles if a.get('category') == category_id]
            summary['categories'][category_id] = {
                'name': category_info['name'],
                'count': len(category_articles),
                'high_importance': len([a for a in category_articles if a.get('importance_level') == 'high']),
                'high_attention': len([a for a in category_articles if a.get('attention_level') == 'high'])
            }
        
        # 重要度レベル別集計
        for level in ['high', 'medium', 'low']:
            level_articles = [a for a in articles if a.get('importance_level') == level]
            summary['importance_levels'][level] = len(level_articles)
        
        # 注目度レベル別集計
        for level in ['high', 'medium', 'low']:
            level_articles = [a for a in articles if a.get('attention_level') == level]
            summary['attention_levels'][level] = len(level_articles)
        
        # トップ記事（重要度・注目度が高いもの）
        top_articles = sorted(
            articles,
            key=lambda x: (x.get('importance_score', 0) + x.get('attention_score', 0)),
            reverse=True
        )[:10]
        
        summary['top_articles'] = [
            {
                'title': a.get('title', ''),
                'link': a.get('link', ''),
                'category': a.get('category_name', ''),
                'importance_score': a.get('importance_score', 0),
                'attention_score': a.get('attention_score', 0),
                'source': a.get('source', '')
            }
            for a in top_articles
        ]
        
        return summary
    
    def _save_analysis_results(self, articles: List[Dict[str, Any]], summary: Dict[str, Any]):
        """分析結果を保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 記事データ保存
        articles_filename = f"data/collected/analyzed_articles_{timestamp}.json"
        os.makedirs(os.path.dirname(articles_filename), exist_ok=True)
        
        with open(articles_filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2, default=str)
        
        # サマリー保存
        summary_filename = f"data/collected/analysis_summary_{timestamp}.json"
        with open(summary_filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"分析結果保存完了: {articles_filename}, {summary_filename}")
    
 