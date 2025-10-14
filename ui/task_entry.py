from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QDateTimeEdit, QPushButton, QLabel
from PyQt6.QtCore import QDateTime, Qt

class TaskEntryWidget(QWidget):
    def __init__(self, add_task_callback, parent=None):
        super().__init__(parent)
        self.add_task_callback = add_task_callback
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.name_label = QLabel("Task Name:")
        layout.addWidget(self.name_label)
        self.task_name_input = QLineEdit()
        layout.addWidget(self.task_name_input)

        self.deadline_label = QLabel("Deadline:")
        layout.addWidget(self.deadline_label)
        self.deadline_input = QDateTimeEdit()
        self.deadline_input.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        layout.addWidget(self.deadline_input)

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

    def add_task(self):
        name = self.task_name_input.text().strip()
        if not name:
            # Optionally show error here
            return
        deadline = self.deadline_input.dateTime().toString(Qt.DateFormat.ISODate)
        self.add_task_callback(name, deadline)
        self.task_name_input.clear()
