"""
クイックテストスクリプト
5件制限でシステムをテスト
"""

import sys
import logging
from datetime import datetime

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def quick_test():
    """5件制限でのクイックテスト"""
    try:
        from modules.collector import NewsCollector
        from modules.analyzer import NewsAnalyzer
        from modules.reporter import NewsletterReporter
        
        logger.info("=== クイックテスト開始（5件制限） ===")
        
        # 1. 情報収集
        logger.info("情報収集開始...")
        collector = NewsCollector()
        articles = collector.collect_all()
        
        if not articles:
            logger.warning("記事が収集されませんでした")
            return False
        
        logger.info(f"収集完了: {len(articles)}件")
        
        # 2. 分析
        logger.info("分析開始...")
        analyzer = NewsAnalyzer()
        analysis_results = analyzer.analyze_articles(articles)
        
        logger.info(f"分析完了: {len(analysis_results['articles'])}件")
        
        # 3. レポート生成
        logger.info("レポート生成開始...")
        
        # デバッグ情報を追加
        logger.info(f"top_articles数: {len(analysis_results['summary']['top_articles'])}")
        if analysis_results['summary']['top_articles']:
            logger.info(f"top_articles[0]のタイプ: {type(analysis_results['summary']['top_articles'][0])}")
            logger.info(f"top_articles[0]: {analysis_results['summary']['top_articles'][0]}")
        
        reporter = NewsletterReporter()
        report_results = reporter.generate_newsletter(analysis_results)
        
        logger.info("レポート生成完了")
        
        # 結果表示
        print("\n=== テスト結果 ===")
        print(f"収集記事数: {len(articles)}")
        print(f"分析記事数: {len(analysis_results['articles'])}")
        print(f"高重要度記事: {analysis_results['summary']['importance_levels'].get('high', 0)}")
        print(f"高注目度記事: {analysis_results['summary']['attention_levels'].get('high', 0)}")
        print(f"HTMLレポート: reports/newsletters/newsletter_{report_results['timestamp']}.html")
        print(f"テキストレポート: reports/newsletters/newsletter_{report_results['timestamp']}.txt")
        
        return True
        
    except Exception as e:
        logger.error(f"テストエラー: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1) 