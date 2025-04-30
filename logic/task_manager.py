import json
from os.path import exists
from datetime import datetime

SAVE_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()

    def add_task(self, title, date_str, tag, start, end, repeat):
        task = {
            "title": title,
            "due": date_str,
            "tag": tag,
            "start": start,
            "end": end,
            "repeat": repeat,
            "complete": False
        }
        self.tasks.append(task)
        self.save_tasks()

    def get_tasks_by_date(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        weekday = date_obj.weekday()
        matched = [t for t in self.tasks if (t["due"] == date_str or (t.get("repeat") and datetime.strptime(t["due"], "%Y-%m-%d").weekday() == weekday))]
        return matched

    def get_completed_tasks(self):
        return [t for t in self.tasks if t.get("complete")]

    def set_task_completion(self, date_str, title, is_complete):
        for task in self.tasks:
            if (task["due"] == date_str or (task.get("repeat") and datetime.strptime(task["due"], "%Y-%m-%d").weekday() == datetime.strptime(date_str, "%Y-%m-%d").weekday())) and task["title"] == title:
                task["complete"] = is_complete
                break

    def delete_task(self, date_str, title):
        self.tasks = [t for t in self.tasks if not ((t["due"] == date_str or (t.get("repeat") and datetime.strptime(t["due"], "%Y-%m-%d").weekday() == datetime.strptime(date_str, "%Y-%m-%d").weekday())) and t["title"] == title)]
        self.save_tasks()

    def load_tasks(self):
        if not exists(SAVE_FILE):
            return []
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)

    def save_tasks(self):
        with open(SAVE_FILE, 'w') as f:
            json.dump(self.tasks, f, indent=2)