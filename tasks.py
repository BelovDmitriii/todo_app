import json
import os
from datetime import datetime

FILENAME = "tasks.json"

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

def get_priority_icon(priority):
    mapping = {
        1: "🔥",
        2: "⚠️",
        3: "📝"
    }
    return mapping.get(priority, "⬜")

#чтение всех задач из файла
def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, 'r', encoding='utf-8') as file:
            return json.load(file)

#запись задач в файл
def save_tasks(tasks):
    with open(FILENAME, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

# отображение задач в консоли
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Список задач пуст.")
        return

    print("Текущие задачи:")
    for i, task in enumerate(tasks, 1):
        status_icon = "✅" if task["done"] else "🔲"
        priority_icon = get_priority_icon(task["priority"])
        print(f"{i}. {status_icon} {priority_icon}  {task['title']}")

#добавление задачи
def add_task(title, priority=2):
    tasks = load_tasks()
    task = {
        "title": title,
        "priority": priority,
        "done": False
    }

    tasks.append(task)
    save_tasks(tasks)

# Удаление задачи
def delete_task():
    tasks = load_tasks()

    if not tasks:
        print("Список задач пуст.")
        return

    print("Список задач:")
    for i, task in enumerate(tasks, 1):
        status = "✅" if task["done"] else "🔲"
        icon = get_priority_icon(str(task["priority"]))
        print(f"{i}. {status} {icon} {task['title']}")

    try:
        index = int(input("Введите номер задачи для удаления: ")) - 1
    except ValueError:
        print("Ошибка: введите число.")
        return

    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"Задача \'{removed['title']}\' удалена.")
    else:
        print("Ошибка: некорректный номер задачи.")

#редактирование задачи в файле
def edit_task(index, new_title):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["title"] = new_title
        save_tasks(tasks)
        return True
    return False

#отметка задач как выполненная/ невыполненная
# [ ] — задача не выполнена
# [x] — задача выполнена
def toggle_task_status(index, complete = True):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = complete
        save_tasks(tasks)
        return 'marked_done' if complete else 'marked_undone'

    return 'invalid_index'

#сортировка задач на выполненные/ невыполненные
# def sort_tasks():
#     tasks = load_tasks()

#     tasks.sort(key=lambda x: x["done"])
#     save_tasks(tasks)

#     print("Задачи отсортированы: невыполненные сначала, выполненные — после.")

#Поиск задач по ключевому слову
def search_tasks(query):
    tasks = load_tasks()
    result = []
    for task in tasks:
        if query.lower() in task["title"].lower():
            result.append(task)
    return result

# Экспорт задач в .txt файл под выбранным именем
def export_tasks(filename):
    tasks = load_tasks()
    with open(filename, "w", encoding="utf-8") as file:
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Экспорт задач - {current_date}\n")
        file.write("=" * 40 + "\n")
        for task in tasks:
            status = "✓" if task["done"] else "✗"
            priority_icon = get_priority_icon(task["priority"])
            file.write(f"{status} {priority_icon} {task['title']}\n")

# Перенос задач из другого файла и добавление в текущий
def import_tasks(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        return

    tasks = load_tasks()
    new_tasks = []

    for line in lines:
        stripped = line.strip()
        if not stripped or "Экспорт задач" in stripped or "===" in stripped:
            continue
        title = stripped.lstrip("✓✗🔥⚠️📝 ").strip()

        new_tasks.append({
            "title": title,
            "priority": 2,
            "done": False
        })

    tasks.extend(new_tasks)
    save_tasks(tasks)

    print(f"Добавлено {len(new_tasks)} задач(и) из файла '{filename}'")
