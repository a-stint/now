import sys
import webbrowser
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QLabel, 
                             QLineEdit, QDateTimeEdit, QListWidget, 
                             QListWidgetItem, QProgressBar, QMessageBox,
                             QInputDialog, QTextEdit)
from PyQt6.QtCore import QDateTime, QTimer, Qt
from PyQt6.QtGui import QFont, QPalette, QColor

class MainWindow(QMainWindow):
    def __init__(self, db_manager, task_manager, currency_system):
        super().__init__()
        self.db_manager = db_manager
        self.task_manager = task_manager
        self.currency_system = currency_system
        
        self.init_ui()
        self.setup_connections()
        self.refresh_display()
        
        # Setup refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_display)
        self.refresh_timer.start(1000)  # Refresh every second
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("Anti-Procrastination Tool")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Currency display
        self.currency_label = QLabel("Virtual Currency: $0.00")
        self.currency_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.currency_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.currency_label)
        
        # Task entry section
        self.setup_task_entry(layout)
        
        # Active tasks display
        self.setup_tasks_display(layout)
        
        # Typing challenge section
        self.setup_typing_section(layout)
        
        # End of day review button
        review_button = QPushButton("End of Day Review")
        review_button.clicked.connect(self.show_review)
        layout.addWidget(review_button)
    
    def setup_task_entry(self, layout):
        """Setup task entry interface"""
        layout.addWidget(QLabel("Add New Task:"))
        
        # Task name input
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Enter task name...")
        layout.addWidget(self.task_name_input)
        
        # Deadline input
        self.deadline_input = QDateTimeEdit()
        self.deadline_input.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        layout.addWidget(self.deadline_input)
        
        # Add task button
        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)
    
    def setup_tasks_display(self, layout):
        """Setup active tasks display"""
        layout.addWidget(QLabel("Today's Tasks:"))
        self.tasks_list = QListWidget()
        layout.addWidget(self.tasks_list)
    
    def setup_typing_section(self, layout):
        """Setup typing challenge section"""
        layout.addWidget(QLabel("Typing Challenge:"))
        
        typing_layout = QHBoxLayout()
        
        # Typemonkey button
        typemonkey_button = QPushButton("Open Typemonkey")
        typemonkey_button.clicked.connect(self.open_typemonkey)
        typing_layout.addWidget(typemonkey_button)
        
        # Speed input
        speed_button = QPushButton("Enter Typing Speed")
        speed_button.clicked.connect(self.enter_typing_speed)
        typing_layout.addWidget(speed_button)
        
        layout.addLayout(typing_layout)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.task_manager.task_deadline_approaching.connect(self.show_urgency_notification)
        self.task_manager.task_deadline_missed.connect(self.handle_missed_deadline)
    
    def add_task(self):
        """Add new task"""
        name = self.task_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a task name")
            return
        
        deadline = self.deadline_input.dateTime().toString(Qt.DateFormat.ISODate)
        task_id = self.task_manager.add_task(name, deadline)
        
        self.task_name_input.clear()
        self.refresh_display()
        
        QMessageBox.information(self, "Success", f"Task '{name}' added successfully!")
    
    def refresh_display(self):
        """Refresh the display with current data"""
        # Update currency display
        balance = self.currency_system.get_balance()
        self.currency_label.setText(f"Virtual Currency: ${balance:.2f}")
        
        # Update tasks list
        self.tasks_list.clear()
        tasks = self.db_manager.get_today_tasks()
        
        for task in tasks:
            task_id, name, user_deadline, artificial_deadline, status, date_created, completed_at = task
            
            # Create task widget
            task_widget = QWidget()
            task_layout = QVBoxLayout(task_widget)
            
            # Task info
            info_label = QLabel(f"{name} - Status: {status}")
            if status == 'pending':
                info_label.setStyleSheet("color: orange;")
            elif status == 'completed':
                info_label.setStyleSheet("color: green;")
            else:
                info_label.setStyleSheet("color: red;")
            
            task_layout.addWidget(info_label)
            
            # Deadline info
            deadline_label = QLabel(f"Artificial Deadline: {artificial_deadline}")
            task_layout.addWidget(deadline_label)
            
            # Complete button for pending tasks
            if status == 'pending':
                complete_button = QPushButton("Complete Task")
                complete_button.clicked.connect(lambda checked, tid=task_id: self.complete_task(tid))
                task_layout.addWidget(complete_button)
            
            # Add to list
            item = QListWidgetItem()
            item.setSizeHint(task_widget.sizeHint())
            self.tasks_list.addItem(item)
            self.tasks_list.setItemWidget(item, task_widget)
    
    def complete_task(self, task_id):
        """Mark task as completed"""
        self.task_manager.complete_task(task_id)
        self.refresh_display()
        QMessageBox.information(self, "Success", "Task completed! +$3 earned!")
    
    def open_typemonkey(self):
        """Open Typemonkey website"""
        webbrowser.open("https://typemonkey.com")
    
    def enter_typing_speed(self):
        """Enter typing speed after Typemonkey test"""
        speed, ok = QInputDialog.getInt(
            self, "Typing Speed", "Enter your typing speed (WPM):", 
            min=1, max=200
        )
        
        if ok:
            is_record = self.currency_system.check_typing_record(speed)
            if is_record:
                QMessageBox.information(
                    self, "New Record!", 
                    f"Congratulations! New typing record: {speed} WPM\n+${self.currency_system.TYPING_RECORD_BONUS} earned!"
                )
            else:
                QMessageBox.information(
                    self, "Speed Recorded", 
                    f"Typing speed recorded: {speed} WPM"
                )
            self.refresh_display()
    
    def show_urgency_notification(self, task_id, message):
        """Show urgency notification"""
        QMessageBox.warning(self, "Deadline Approaching!", message)
    
    def handle_missed_deadline(self, task_id, message):
        """Handle missed deadline"""
        QMessageBox.critical(self, "Deadline Missed!", f"{message}\n-$5 penalty applied")
        self.refresh_display()
    
    def show_review(self):
        """Show end of day review"""
        tasks = self.db_manager.get_today_tasks()
        completed = len([t for t in tasks if t[4] == 'completed'])
        missed = len([t for t in tasks if t[4] == 'missed'])
        pending = len([t for t in tasks if t[4] == 'pending'])
        
        balance = self.currency_system.get_balance()
        
        review_text = f"""
        End of Day Review:
        
        Tasks Completed: {completed}
        Tasks Missed: {missed}
        Tasks Pending: {pending}
        
        Current Balance: ${balance:.2f}
        
        {"Great job today!" if completed > missed else "Room for improvement tomorrow!"}
        """
        
        QMessageBox.information(self, "Daily Review", review_text)
