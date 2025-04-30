from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QLabel, QDateEdit, QTimeEdit, QCheckBox
from PyQt5.QtCore import QDate, QTime

class TaskDialog(QDialog):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.setWindowTitle("Add Task")

        self.layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.layout.addWidget(QLabel("Task Title:"))
        self.layout.addWidget(self.title_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.layout.addWidget(QLabel("Due Date:"))
        self.layout.addWidget(self.date_input)

        self.start_time = QTimeEdit()
        self.start_time.setTime(QTime.currentTime())
        self.end_time = QTimeEdit()
        self.end_time.setTime(QTime.currentTime().addSecs(3600))
        self.layout.addWidget(QLabel("Start Time:"))
        self.layout.addWidget(self.start_time)
        self.layout.addWidget(QLabel("End Time:"))
        self.layout.addWidget(self.end_time)

        self.tag_input = QLineEdit()
        self.layout.addWidget(QLabel("Custom Tag:"))
        self.layout.addWidget(self.tag_input)

        self.repeat_checkbox = QCheckBox("Repeat Weekly on this Day")
        self.layout.addWidget(self.repeat_checkbox)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.add_task)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)

    def add_task(self):
        title = self.title_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        tag = self.tag_input.text() or "General"
        start = self.start_time.time().toString("HH:mm")
        end = self.end_time.time().toString("HH:mm")
        repeat = self.repeat_checkbox.isChecked()

        if title:
            self.task_manager.add_task(title, date, tag, start, end, repeat)
        self.accept()