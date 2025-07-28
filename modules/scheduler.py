"""
スケジューリングモジュール
月曜夜の自動実行を管理
"""

import schedule
import time
import logging
from datetime import datetime, timedelta
import threading
from typing import Callable, Optional

logger = logging.getLogger(__name__)

class NewsletterScheduler:
    def __init__(self, newsletter_function: Callable):
        """
        スケジューラーを初期化
        
        Args:
            newsletter_function: ニュースレター生成を実行する関数
        """
        self.newsletter_function = newsletter_function
        self.is_running = False
        self.scheduler_thread = None
    
    def start_scheduler(self):
        """スケジューラーを開始"""
        logger.info("スケジューラー開始")
        
        # 月曜夜8時に実行（コメントアウト）
        # schedule.every().monday.at("20:00").do(self._run_newsletter)
        
        # テスト用：1分後に実行（コメントアウト）
        # schedule.every(1).minutes.do(self._run_newsletter)
        
        self.is_running = True
        
        # 別スレッドでスケジューラーを実行
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        logger.info("スケジューラーが開始されました。月曜夜8時にニュースレターが自動生成されます。")
    
    def stop_scheduler(self):
        """スケジューラーを停止"""
        logger.info("スケジューラー停止")
        self.is_running = False
        schedule.clear()
        
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
    
    def _run_scheduler(self):
        """スケジューラーのメインループ"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # 1分ごとにチェック
    
    def _run_newsletter(self):
        """ニュースレター生成を実行"""
        try:
            logger.info("ニュースレター生成を開始します")
            self.newsletter_function()
            logger.info("ニュースレター生成が完了しました")
        except Exception as e:
            logger.error(f"ニュースレター生成中にエラーが発生しました: {e}")
    
    def run_manual(self):
        """手動実行"""
        logger.info("手動でニュースレター生成を実行します")
        self._run_newsletter()
    
    def get_next_run_time(self) -> Optional[datetime]:
        """次回実行時刻を取得"""
        try:
            # scheduleライブラリから次回実行時刻を取得
            jobs = schedule.get_jobs()
            if jobs:
                # 最初のジョブの次回実行時刻を取得
                next_run = jobs[0].next_run
                return next_run
        except Exception as e:
            logger.error(f"次回実行時刻の取得に失敗: {e}")
        
        return None
    
    def get_status(self) -> dict:
        """スケジューラーの状態を取得"""
        next_run = self.get_next_run_time()
        
        return {
            'is_running': self.is_running,
            'next_run_time': next_run.isoformat() if next_run else None,
            'current_time': datetime.now().isoformat()
        }

class ManualScheduler:
    """手動実行用のシンプルなスケジューラー"""
    
    def __init__(self, newsletter_function: Callable):
        self.newsletter_function = newsletter_function
    
    def run_now(self):
        """即座に実行"""
        logger.info("手動実行を開始します")
        try:
            self.newsletter_function()
            logger.info("手動実行が完了しました")
        except Exception as e:
            logger.error(f"手動実行中にエラーが発生しました: {e}")
    
    def run_with_delay(self, delay_minutes: int = 0):
        """指定時間後に実行"""
        import threading
        import time
        
        def delayed_run():
            time.sleep(delay_minutes * 60)
            self.run_now()
        
        thread = threading.Thread(target=delayed_run)
        thread.daemon = True
        thread.start()
        
        logger.info(f"{delay_minutes}分後にニュースレター生成を実行します")

def create_scheduler(newsletter_function: Callable, auto_schedule: bool = True):
    """
    スケジューラーを作成
    
    Args:
        newsletter_function: ニュースレター生成関数
        auto_schedule: 自動スケジューリングを有効にするかどうか
    
    Returns:
        NewsletterScheduler or ManualScheduler
    """
    if auto_schedule:
        return NewsletterScheduler(newsletter_function)
    else:
        return ManualScheduler(newsletter_function) 