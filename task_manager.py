import datetime
from PyQt6.QtCore import QTimer, QObject, pyqtSignal

class TaskManager(QObject):
    task_deadline_approaching = pyqtSignal(int, str)  # task_id, task_name
    task_deadline_missed = pyqtSignal(int, str)
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.timers = {}
        self.setup_deadline_monitoring()
    
    def calculate_artificial_deadline(self, user_deadline_str):
        """Calculate artificial deadline (25% earlier or 11 AM)"""
        user_deadline = datetime.datetime.fromisoformat(user_deadline_str)
        
        # Calculate 25% earlier
        time_diff = user_deadline - datetime.datetime.now()
        reduced_diff = time_diff * 0.75
        artificial_deadline = datetime.datetime.now() + reduced_diff
        
        # Check if 11 AM today is earlier
        eleven_am = datetime.datetime.combine(
            datetime.date.today(), 
            datetime.time(11, 0)
        )
        
        if eleven_am < artificial_deadline and eleven_am > datetime.datetime.now():
            artificial_deadline = eleven_am
        
        return artificial_deadline.isoformat()
    
    def add_task(self, name, user_deadline):
        """Add new task with artificial deadline"""
        artificial_deadline = self.calculate_artificial_deadline(user_deadline)
        task_id = self.db_manager.add_task(name, user_deadline, artificial_deadline)
        self.setup_task_timer(task_id, artificial_deadline)
        return task_id
    
    def setup_task_timer(self, task_id, deadline_str):
        """Setup timer for task deadline monitoring"""
        deadline = datetime.datetime.fromisoformat(deadline_str)
        now = datetime.datetime.now()
        
        if deadline > now:
            # Timer for deadline approach warning (30 minutes before)
            warning_time = deadline - datetime.timedelta(minutes=30)
            if warning_time > now:
                warning_timer = QTimer()
                warning_timer.timeout.connect(
                    lambda: self.task_deadline_approaching.emit(task_id, "Task deadline approaching!")
                )
                warning_timer.setSingleShot(True)
                warning_timer.start(int((warning_time - now).total_seconds() * 1000))
            
            # Timer for actual deadline
            deadline_timer = QTimer()
            deadline_timer.timeout.connect(
                lambda: self.handle_deadline_missed(task_id)
            )
            deadline_timer.setSingleShot(True)
            deadline_timer.start(int((deadline - now).total_seconds() * 1000))
    
    def handle_deadline_missed(self, task_id):
        """Handle when task deadline is missed"""
        self.db_manager.update_task_status(task_id, 'missed')
        self.db_manager.add_currency_transaction(-5, f'Missed deadline for task {task_id}')
        self.task_deadline_missed.emit(task_id, "Task deadline missed!")
    
    def complete_task(self, task_id):
        """Mark task as completed and award currency"""
        self.db_manager.update_task_status(task_id, 'completed')
        self.db_manager.add_currency_transaction(3, f'Completed task {task_id}')
    
    def setup_deadline_monitoring(self):
        """Setup monitoring for existing tasks"""
        tasks = self.db_manager.get_today_tasks()
        for task in tasks:
            if task[4] == 'pending':  # status column
                self.setup_task_timer(task[0], task[3])  # id, artificial_deadline
