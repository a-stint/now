import sqlite3
import datetime
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        self.db_path = Path("data/app_data.db")
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tasks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    user_deadline TEXT NOT NULL,
                    artificial_deadline TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    date_created TEXT NOT NULL,
                    completed_at TEXT
                )
            ''')
            
            # Virtual currency table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS currency_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    reason TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            # Typing scores table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS typing_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    wpm INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    is_record BOOLEAN DEFAULT 0
                )
            ''')
            
            conn.commit()
    
    def add_task(self, name, user_deadline, artificial_deadline):
        """Add a new task to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (name, user_deadline, artificial_deadline, date_created)
                VALUES (?, ?, ?, ?)
            ''', (name, user_deadline, artificial_deadline, datetime.datetime.now().isoformat()))
            conn.commit()
            return cursor.lastrowid
    
    def get_today_tasks(self):
        """Get all tasks for today"""
        today = datetime.date.today().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM tasks 
                WHERE date(date_created) = ?
                ORDER BY artificial_deadline
            ''', (today,))
            return cursor.fetchall()
    
    def update_task_status(self, task_id, status):
        """Update task completion status"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks SET status = ?, completed_at = ?
                WHERE id = ?
            ''', (status, datetime.datetime.now().isoformat(), task_id))
            conn.commit()
    
    def add_currency_transaction(self, amount, reason):
        """Add currency transaction"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO currency_transactions (amount, reason, timestamp)
                VALUES (?, ?, ?)
            ''', (amount, reason, datetime.datetime.now().isoformat()))
            conn.commit()
    
    def get_currency_balance(self):
        """Get current virtual currency balance"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(amount) FROM currency_transactions')
            result = cursor.fetchone()[0]
            return result if result else 50.0  # Starting balance
