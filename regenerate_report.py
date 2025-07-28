"""
既存の分析データからレポートを再生成するスクリプト
体裁調整やテンプレート変更後に使用
"""

import json
import sys
import logging
from datetime import datetime
from modules.reporter import NewsletterReporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def regenerate_report(analysis_file_path: str):
    """既存の分析データからレポートを再生成"""
    try:
        # 分析データを読み込み
        with open(analysis_file_path, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        logger.info(f"分析データ読み込み完了: {len(analysis_data['articles'])}件")
        
        # レポート生成
        reporter = NewsletterReporter()
        report_results = reporter.generate_newsletter(analysis_data)
        
        # 結果表示
        print("\n=== レポート再生成完了 ===")
        print(f"HTMLレポート: reports/newsletters/newsletter_{report_results['timestamp']}.html")
        print(f"テキストレポート: reports/newsletters/newsletter_{report_results['timestamp']}.txt")
        
        return True
        
    except Exception as e:
        logger.error(f"レポート再生成エラー: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python regenerate_report.py <分析データのパス>")
        print("例: python regenerate_report.py data/collected/analyzed_articles_20250728_160041.json")
        sys.exit(1)
    
    analysis_file = sys.argv[1]
    success = regenerate_report(analysis_file)
    sys.exit(0 if success else 1)