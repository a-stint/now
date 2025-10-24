import datetime
import sqlite3

class CurrencySystem:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.TASK_COMPLETION_REWARD = 1
        self.DEADLINE_MISS_PENALTY = 3
        self.TYPING_RECORD_BONUS = 2
    
    def get_balance(self):
        """Get current virtual currency balance"""
        return self.db_manager.get_currency_balance()
    
    def reward_task_completion(self, task_id):
        """Reward user for completing task"""
        self.db_manager.add_currency_transaction(
            self.TASK_COMPLETION_REWARD,
            f"Task {task_id} completed on time"
        )
    
    def penalize_missed_deadline(self, task_id):
        """Penalize user for missing deadline"""
        self.db_manager.add_currency_transaction(
            -self.DEADLINE_MISS_PENALTY,
            f"Missed deadline for task {task_id}"
        )
    
    def check_typing_record(self, new_wpm):
        """Check if new typing speed is a record and reward accordingly"""
        with sqlite3.connect(self.db_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(wpm) FROM typing_scores')
            current_record = cursor.fetchone()[0] or 0
            
            if new_wpm > current_record:
                # New record!
                cursor.execute('''
                    INSERT INTO typing_scores (wpm, date, is_record)
                    VALUES (?, ?, 1)
                ''', (new_wpm, datetime.date.today().isoformat()))
                
                self.db_manager.add_currency_transaction(
                    self.TYPING_RECORD_BONUS,
                    f"New typing record: {new_wpm} WPM"
                )
                conn.commit()
                return True
            else:
                cursor.execute('''
                    INSERT INTO typing_scores (wpm, date, is_record)
                    VALUES (?, ?, 0)
                ''', (new_wpm, datetime.date.today().isoformat()))
                conn.commit()
                return False
