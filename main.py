import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from database import DatabaseManager
from task_manager import TaskManager
from currency_sys import CurrencySystem
from ui.main_wind import MainWindow
from notification import NotificationManager

def main():
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Anti-Procrastination Tool")
    
    # Initialize core systems
    db_manager = DatabaseManager()
    task_manager = TaskManager(db_manager)
    currency_system = CurrencySystem(db_manager)
    notification_manager = NotificationManager()
    
    # Create and show main window
    main_window = MainWindow(db_manager, task_manager, currency_system)
    main_window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
