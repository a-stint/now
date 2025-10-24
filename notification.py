from plyer import notification
import os

class NotificationManager:
    def __init__(self):
        self.app_name = "Anti-Procrastination Tool"
    
    def send_urgency_notification(self, task_name, minutes_remaining):
        """Send urgency notification for approaching deadline"""
        notification.notify(
            title="⚠️ Deadline Approaching!",
            message=f"'{task_name}' deadline in {minutes_remaining} minutes!",
            app_name=self.app_name,
            timeout=10
        )
    
    def send_deadline_missed(self, task_name):
        """Send notification for missed deadline"""
        notification.notify(
            title="❌ Deadline Missed!",
            message=f"'{task_name}' deadline has passed. -$3 penalty applied.",
            app_name=self.app_name,
            timeout=10
        )
    
    def send_task_completed(self, task_name):
        """Send notification for completed task"""
        notification.notify(
            title="✅ Task Completed!",
            message=f"'{task_name}' completed successfully! +$1 earned!",
            app_name=self.app_name,
            timeout=5
        )
    
    def send_typing_record(self, wpm):
        """Send notification for new typing record"""
        notification.notify(
            title="🏆 New Typing Record!",
            message=f"New personal best: {wpm} WPM! +$2 bonus earned!",
            app_name=self.app_name,
            timeout=8
        )
