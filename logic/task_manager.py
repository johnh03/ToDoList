import json
from os.path import exists
from datetime import datetime

SAVE_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()

    def add_task(self, title, date_str, tag, start, end, repeat, description=""):
        task = {
            "title": title,
            "due": date_str,
            "tag": tag,
            "start": start,
            "end": end,
            "repeat": repeat,
            "complete": False,
            "completed_dates": [],
            "description": description
        }
        self.tasks.append(task)
        self.save_tasks()

    def get_tasks_by_date(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        weekday = date_obj.weekday()
        matched = [t for t in self.tasks if (t["due"] == date_str or (t.get("repeat") and datetime.strptime(t["due"], "%Y-%m-%d").weekday() == weekday))]
        return matched

    def get_completed_tasks(self):
        completed = []
        for t in self.tasks:
            if t.get("repeat"):
                for d in t.get("completed_dates", []):
                    completed.append({**t, "due": d})
            elif t.get("complete"):
                completed.append(t)
        return completed

    def set_task_completion(self, date_str, title, is_complete):
        for task in self.tasks:
            if task["title"] == title and (task["due"] == date_str or (task.get("repeat") and datetime.strptime(task["due"], "%Y-%m-%d").weekday() == datetime.strptime(date_str, "%Y-%m-%d").weekday())):
                if task.get("repeat"):
                    if "completed_dates" not in task:
                        task["completed_dates"] = []
                    if is_complete and date_str not in task["completed_dates"]:
                        task["completed_dates"].append(date_str)
                else:
                    task["complete"] = is_complete
                break

    def delete_task(self, date_str, title):
        self.tasks = [t for t in self.tasks if not (t["title"] == title and (t["due"] == date_str or (t.get("repeat") and datetime.strptime(t["due"], "%Y-%m-%d").weekday() == datetime.strptime(date_str, "%Y-%m-%d").weekday())))]
        self.save_tasks()

    def load_tasks(self):
        if not exists(SAVE_FILE):
            return []
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)

    def save_tasks(self):
        with open(SAVE_FILE, 'w') as f:
            json.dump(self.tasks, f, indent=2)
