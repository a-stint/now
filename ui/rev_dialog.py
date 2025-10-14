from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class ReviewDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("End of Day Review")
        self.setMinimumSize(400, 300)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.review_label = QLabel("", self)
        self.layout.addWidget(self.review_label)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.accept)
        self.layout.addWidget(self.close_button)

    def load_data(self):
        tasks = self.db_manager.get_today_tasks()
        completed = len([t for t in tasks if t[4] == 'completed'])
        missed = len([t for t in tasks if t[4] == 'missed'])
        pending = len([t for t in tasks if t[4] == 'pending'])

        balance = self.db_manager.get_currency_balance()

        review_text = f"""
        Tasks Completed: {completed}
        Tasks Missed: {missed}
        Tasks Pending: {pending}

        Current Virtual Currency Balance: ${balance:.2f}

        {'Great job today!' if completed > missed else 'Room for improvement tomorrow!'}
        """
        self.review_label.setText(review_text)
