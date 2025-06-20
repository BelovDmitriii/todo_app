from core.db import get_tasks

tasks = get_tasks()
for task in tasks:
    print(task.id, task.title, task.priority, task.done)
print("Hello")

# python -m data.view_tasks
