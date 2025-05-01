from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QTimeEdit, QCheckBox, QDialogButtonBox, QTextEdit
from PyQt5.QtCore import QTime
from datetime import datetime

class TaskDialog(QDialog):
    def __init__(self, task_manager):
        super().__init__()
        self.setWindowTitle("Add Task")
        self.task_manager = task_manager

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        layout.addWidget(QLabel("Task Title:"))
        layout.addWidget(self.title_input)

        self.start_input = QTimeEdit()
        self.start_input.setTime(QTime.currentTime())
        layout.addWidget(QLabel("Start Time:"))
        layout.addWidget(self.start_input)

        self.end_input = QTimeEdit()
        self.end_input.setTime(QTime.currentTime().addSecs(3600))
        layout.addWidget(QLabel("End Time:"))
        layout.addWidget(self.end_input)

        self.tag_input = QLineEdit()
        layout.addWidget(QLabel("Task Tag (e.g., Work, Chores, etc.):"))
        layout.addWidget(self.tag_input)

        self.description_input = QTextEdit()
        layout.addWidget(QLabel("Task Description:"))
        layout.addWidget(self.description_input)

        self.repeat_checkbox = QCheckBox("Repeat Weekly")
        layout.addWidget(self.repeat_checkbox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def accept(self):
        title = self.title_input.text().strip()
        if not title:
            return

        today = datetime.now().strftime("%Y-%m-%d")

        self.task_manager.add_task(
    title,
    today,
    self.tag_input.text().strip() or "General",
    self.start_input.time().toString("HH:mm"),
    self.end_input.time().toString("HH:mm"),
    self.repeat_checkbox.isChecked(),
    self.description_input.toPlainText().strip()
)

        super().accept()