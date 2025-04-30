from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QCalendarWidget, QPushButton, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QTabWidget, QLineEdit, QComboBox
from PyQt5.QtCore import QDate, Qt
from ui.task_dialog import TaskDialog
from logic.task_manager import TaskManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do Calendar")
        self.setGeometry(100, 100, 1000, 600)

        self.task_manager = TaskManager()

        self.tabs = QTabWidget()

        self.main_tab = QWidget()
        self.history_tab = QWidget()

        self.setup_main_tab()
        self.setup_history_tab()

        self.tabs.addTab(self.main_tab, "Today + Calendar")
        self.tabs.addTab(self.history_tab, "Completed Tasks")

        self.setCentralWidget(self.tabs)
        self.calendar.update()

    def setup_main_tab(self):
        self.main_layout = QHBoxLayout(self.main_tab)

        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.load_tasks_for_selected_date)
        self.calendar.setGridVisible(True)
        self.calendar.paintCell = self.paint_calendar_cell

        self.task_list = QListWidget()

        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.open_task_dialog)

        self.delete_task_button = QPushButton("Delete Selected Task")
        self.delete_task_button.clicked.connect(self.delete_selected_task)

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(QLabel("Tasks for selected day:"))
        self.right_layout.addWidget(self.task_list)
        self.right_layout.addWidget(self.add_task_button)
        self.right_layout.addWidget(self.delete_task_button)

        self.main_layout.addWidget(self.calendar)
        right_container = QWidget()
        right_container.setLayout(self.right_layout)
        self.main_layout.addWidget(right_container)

        self.load_tasks_for_selected_date(QDate.currentDate())

    def setup_history_tab(self):
        self.history_layout = QVBoxLayout(self.history_tab)
        self.history_filter_input = QLineEdit()
        self.history_filter_input.setPlaceholderText("Filter by keyword...")
        self.history_filter_input.textChanged.connect(self.load_completed_tasks)

        self.tag_filter = QComboBox()
        self.tag_filter.addItem("All Tags")
        self.tag_filter.addItems(sorted(set([t['tag'] for t in self.task_manager.tasks])))
        self.tag_filter.currentIndexChanged.connect(self.load_completed_tasks)

        self.history_list = QListWidget()

        self.history_layout.addWidget(QLabel("Completed Tasks:"))
        self.history_layout.addWidget(self.history_filter_input)
        self.history_layout.addWidget(self.tag_filter)
        self.history_layout.addWidget(self.history_list)
        self.load_completed_tasks()

    def load_tasks_for_selected_date(self, date):
        self.task_list.clear()
        self.calendar.update()
        date_str = date.toString("yyyy-MM-dd")
        self.current_date = date_str
        tasks = self.task_manager.get_tasks_by_date(date_str)
        for task in tasks:
            if not task.get("complete"):
                item = QListWidgetItem(f"[{task['tag']}] {task['title']} ({task['start']} - {task['end']})")
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                self.task_list.addItem(item)
        self.task_list.itemChanged.connect(self.mark_complete)

    def open_task_dialog(self):
        dialog = TaskDialog(self.task_manager)
        if dialog.exec_():
            self.load_tasks_for_selected_date(self.calendar.selectedDate())
            self.calendar.update()
            self.load_completed_tasks()

    def mark_complete(self, item):
        text = item.text()
        if not text:
            return
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        title = text.split(']')[1].split('(')[0].strip()
        self.task_manager.set_task_completion(date, title, True)
        self.task_manager.save_tasks()
        self.task_list.takeItem(self.task_list.row(item))
        self.calendar.update()
        self.load_completed_tasks()

    def delete_selected_task(self):
        selected = self.task_list.currentItem()
        if selected:
            title = selected.text().split(']')[1].split('(')[0].strip()
            self.task_manager.delete_task(self.current_date, title)
            self.load_tasks_for_selected_date(self.calendar.selectedDate())
            self.calendar.update()

    def load_completed_tasks(self):
        self.history_list.clear()
        keyword = self.history_filter_input.text().lower()
        selected_tag = self.tag_filter.currentText()
        for task in self.task_manager.get_completed_tasks():
            if (keyword in task['title'].lower()) and (selected_tag == "All Tags" or task['tag'] == selected_tag):
                self.history_list.addItem(f"{task['due']} - {task['title']} [{task['tag']}] ({task['start']} - {task['end']})")

    def paint_calendar_cell(self, painter, rect, date):
        from PyQt5.QtGui import QColor, QBrush
        QCalendarWidget.paintCell(self.calendar, painter, rect, date)
        date_str = date.toString("yyyy-MM-dd")
        tasks = self.task_manager.get_tasks_by_date(date_str)
        if any(not t.get("complete") for t in tasks):
            painter.save()
            painter.setBrush(QBrush(QColor(200, 230, 201, 150)))
            painter.drawRect(rect)
            painter.restore()
