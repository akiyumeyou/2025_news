"""
AI最新情報キャッチアップシステム
メイン実行ファイル
"""

import os
import sys
import logging
from datetime import datetime
import argparse
from typing import Optional

# モジュールのインポート
from modules.collector import NewsCollector
from modules.analyzer import NewsAnalyzer
from modules.reporter import NewsletterReporter
from modules.scheduler import create_scheduler

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('newsletter.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class AINewsletterSystem:
    def __init__(self):
        self.collector = NewsCollector()
        self.analyzer = NewsAnalyzer()
        self.reporter = NewsletterReporter()
        self.scheduler = None
    
    def run_full_pipeline(self) -> dict:
        """完全なパイプラインを実行"""
        logger.info("AI最新情報キャッチアップシステム開始")
        
        try:
            # 1. 情報収集
            logger.info("=== 情報収集フェーズ ===")
            articles = self.collector.collect_all()
            logger.info(f"収集完了: {len(articles)}件の記事")
            
            if not articles:
                logger.warning("収集された記事がありません")
                return {'error': 'No articles collected'}
            
            # 2. 分析
            logger.info("=== 分析フェーズ ===")
            analysis_results = self.analyzer.analyze_articles(articles)
            logger.info(f"分析完了: {len(analysis_results['articles'])}件の記事を分析")
            
            # 3. レポート生成
            logger.info("=== レポート生成フェーズ ===")
            report_results = self.reporter.generate_newsletter(analysis_results)
            logger.info("レポート生成完了")
            
            # 結果サマリー
            summary = {
                'collected_articles': len(articles),
                'analyzed_articles': len(analysis_results['articles']),
                'high_importance': analysis_results['summary']['importance_levels'].get('high', 0),
                'high_attention': analysis_results['summary']['attention_levels'].get('high', 0),
                'timestamp': report_results['timestamp'],
                'html_file': f"reports/newsletters/newsletter_{report_results['timestamp']}.html",
                'text_file': f"reports/newsletters/newsletter_{report_results['timestamp']}.txt"
            }
            
            logger.info("=== 実行完了 ===")
            logger.info(f"収集記事数: {summary['collected_articles']}")
            logger.info(f"分析記事数: {summary['analyzed_articles']}")
            logger.info(f"高重要度記事: {summary['high_importance']}")
            logger.info(f"高注目度記事: {summary['high_attention']}")
            logger.info(f"HTMLレポート: {summary['html_file']}")
            logger.info(f"テキストレポート: {summary['text_file']}")
            
            return summary
            
        except Exception as e:
            logger.error(f"パイプライン実行中にエラーが発生: {e}")
            return {'error': str(e)}
    
    def start_scheduler(self):
        """スケジューラーを開始"""
        self.scheduler = create_scheduler(self.run_full_pipeline, auto_schedule=True)
        self.scheduler.start_scheduler()
        
        try:
            # スケジューラーを継続実行
            while True:
                import time
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("スケジューラーを停止します")
            if self.scheduler:
                self.scheduler.stop_scheduler()
    
    def run_manual(self):
        """手動実行"""
        return self.run_full_pipeline()
    
    def get_status(self) -> dict:
        """システム状態を取得"""
        status = {
            'system_time': datetime.now().isoformat(),
            'scheduler_running': False,
            'next_run_time': None
        }
        
        if self.scheduler:
            scheduler_status = self.scheduler.get_status()
            status.update(scheduler_status)
        
        return status

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='AI最新情報キャッチアップシステム')
    parser.add_argument('--mode', choices=['manual', 'scheduler', 'status'], 
                       default='manual', help='実行モード')
    parser.add_argument('--auto-schedule', action='store_true', 
                       help='自動スケジューリングを有効にする')
    
    args = parser.parse_args()
    
    # システム初期化
    system = AINewsletterSystem()
    
    if args.mode == 'manual':
        logger.info("手動実行モード")
        result = system.run_manual()
        
        if 'error' in result:
            logger.error(f"実行エラー: {result['error']}")
            sys.exit(1)
        else:
            logger.info("手動実行完了")
            print(f"\n=== 実行結果 ===")
            print(f"収集記事数: {result['collected_articles']}")
            print(f"分析記事数: {result['analyzed_articles']}")
            print(f"高重要度記事: {result['high_importance']}")
            print(f"高注目度記事: {result['high_attention']}")
            print(f"HTMLレポート: {result['html_file']}")
            print(f"テキストレポート: {result['text_file']}")
    
    elif args.mode == 'scheduler':
        logger.info("スケジューラーモード")
        system.start_scheduler()
    
    elif args.mode == 'status':
        status = system.get_status()
        print("=== システム状態 ===")
        print(f"現在時刻: {status['system_time']}")
        print(f"スケジューラー実行中: {status['scheduler_running']}")
        if status['next_run_time']:
            print(f"次回実行時刻: {status['next_run_time']}")

if __name__ == "__main__":
    main() 