"""
システムテストスクリプト
"""

import sys
import logging
from datetime import datetime

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_collector():
    """情報収集モジュールのテスト"""
    try:
        from modules.collector import NewsCollector
        
        logger.info("情報収集モジュールのテスト開始")
        collector = NewsCollector()
        
        # RSS収集テスト
        articles = collector.collect_rss_feeds()
        logger.info(f"RSS収集テスト: {len(articles)}件の記事を収集")
        
        return len(articles) > 0
        
    except Exception as e:
        logger.error(f"情報収集テストエラー: {e}")
        return False

def test_analyzer():
    """分析モジュールのテスト"""
    try:
        from modules.analyzer import NewsAnalyzer
        
        logger.info("分析モジュールのテスト開始")
        analyzer = NewsAnalyzer()
        
        # テスト用の記事データ
        test_articles = [
            {
                'title': 'OpenAI releases new GPT-4 model with improved capabilities',
                'description': 'OpenAI has announced a new version of GPT-4 with enhanced performance and safety features.',
                'link': 'https://example.com/article1',
                'published_date': datetime.now(),
                'source': 'Test Source',
                'source_type': 'test',
                'category': 'general',
                'priority': 'high'
            },
            {
                'title': 'GitHub Copilot introduces new code generation features',
                'description': 'GitHub Copilot now supports more programming languages and improved code suggestions.',
                'link': 'https://example.com/article2',
                'published_date': datetime.now(),
                'source': 'Test Source',
                'source_type': 'test',
                'category': 'general',
                'priority': 'medium'
            }
        ]
        
        # 分析実行
        results = analyzer.analyze_articles(test_articles)
        logger.info(f"分析テスト: {len(results['articles'])}件の記事を分析")
        
        return len(results['articles']) > 0
        
    except Exception as e:
        logger.error(f"分析テストエラー: {e}")
        return False

def test_reporter():
    """レポート生成モジュールのテスト"""
    try:
        from modules.reporter import NewsletterReporter
        
        logger.info("レポート生成モジュールのテスト開始")
        reporter = NewsletterReporter()
        
        # テスト用の分析結果
        test_analysis = {
            'articles': [
                {
                    'title': 'Test Article 1',
                    'link': 'https://example.com/test1',
                    'description': 'This is a test article for the newsletter.',
                    'category': 'programming',
                    'category_name': 'プログラミング',
                    'importance_score': 0.8,
                    'attention_score': 0.7,
                    'importance_level': 'high',
                    'attention_level': 'high',
                    'source': 'Test Source'
                }
            ],
            'summary': {
                'total_articles': 1,
                'importance_levels': {'high': 1, 'medium': 0, 'low': 0},
                'attention_levels': {'high': 1, 'medium': 0, 'low': 0},
                'top_articles': [
                    {
                        'title': 'Test Article 1',
                        'link': 'https://example.com/test1',
                        'category': 'プログラミング',
                        'importance_score': 0.8,
                        'attention_score': 0.7,
                        'source': 'Test Source'
                    }
                ]
            }
        }
        
        # レポート生成
        results = reporter.generate_newsletter(test_analysis)
        logger.info("レポート生成テスト完了")
        
        return 'html_content' in results and 'text_content' in results
        
    except Exception as e:
        logger.error(f"レポート生成テストエラー: {e}")
        return False

def test_config():
    """設定ファイルのテスト"""
    try:
        logger.info("設定ファイルのテスト開始")
        
        # カテゴリ設定のテスト
        from config.categories import CATEGORIES
        logger.info(f"カテゴリ設定: {len(CATEGORIES)}個のカテゴリ")
        
        # ソース設定のテスト
        from config.sources import RSS_SOURCES
        logger.info(f"RSSソース設定: {len(RSS_SOURCES)}個のソース")
        
        return True
        
    except Exception as e:
        logger.error(f"設定テストエラー: {e}")
        return False

def run_all_tests():
    """全てのテストを実行"""
    logger.info("=== システムテスト開始 ===")
    
    tests = [
        ("設定ファイル", test_config),
        ("情報収集", test_collector),
        ("分析", test_analyzer),
        ("レポート生成", test_reporter)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name}テスト ---")
        try:
            result = test_func()
            results[test_name] = result
            status = "成功" if result else "失敗"
            logger.info(f"{test_name}テスト: {status}")
        except Exception as e:
            results[test_name] = False
            logger.error(f"{test_name}テスト: エラー - {e}")
    
    # 結果サマリー
    logger.info("\n=== テスト結果サマリー ===")
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓" if result else "✗"
        logger.info(f"{status} {test_name}")
    
    logger.info(f"\n総合結果: {passed}/{total} テスト成功")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 