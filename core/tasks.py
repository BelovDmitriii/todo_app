import json
import os
from config import TASKS_FILE as FILENAME
from core.models import Task

__all__ = ["load_tasks", "save_tasks", "get_task_list", "sort_tasks"]

def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, 'r', encoding='utf-8') as file:
        raw_tasks = json.load(file)
        return [Task.from_dict(t) for t in raw_tasks]


def save_tasks(tasks):
    with open(FILENAME, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def get_task_list(tasks: list) -> str:
    if not tasks:
        return "У вас пока нет задач ✅"

    message = "Ваши задачи:\n\n"

    for i, task in enumerate(tasks, start=1):
        status = "✅" if task.get("done") else "🔲"
        priority_icon = {3: "🔥", 2: "⚠️", 1: "📝"}.get(task["priority"], "")
        message += f"{i}. {status} {priority_icon} {task['title']}\n\n"

    return message

def sort_tasks(tasks):
    return sorted(
        tasks,
        key=lambda task: (task["done"], -task["priority"])
    )
