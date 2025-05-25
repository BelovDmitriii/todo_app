from datetime import datetime
import re

def get_priority_icon(priority):
    mapping = {
        "1": "🔥",
        "2": "⚠️",
        "3": "📝"
    }
    return mapping.get(priority, "⬜")

# отображение задач в консоли
def list_tasks():
    tasks = read_tasks()
    if not tasks:
        print("Список задач пуст.")
        return

    print("Текущие задачи:")
    for i, task in enumerate(tasks, 1):
        status = "[x]" if "[x]" in task else "[ ]"
        status_icon = "✅" if status == "[x]" else "🔲"

        # Ищем приоритет вида [1], [2], [3]
        match = re.search(r"\[(\d)\]", task)
        if match:
            priority_number = match.group(1)
        else:
            priority_number = "2"  # значение по умолчанию

        priority_icon = get_priority_icon(priority_number)

        # Убираем статус и приоритет из текста задачи
        clean_text = re.sub(r"\[.\]\s*\[.\]", "", task).strip()

        print(f"{i}. {status_icon} {priority_icon}  {clean_text}")

#добавление задачи
def add_task(task_text, priority=2, filename = 'tasks.txt'):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"[ ] [{priority}] {task_text}\n")

#чтение всех задач из файла
def read_tasks(filename = 'tasks.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

#запись задач в файл
def write_tasks(tasks, filename = 'tasks.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        for task in tasks:
            if not task.endswith('\n'):
                task += '\n'
            file.write(task)

#редактирование задачи в файле
def edit_task(index, new_text):
    tasks = read_tasks()
    if 0 <= index < len(tasks):
        current = tasks[index].strip()

        status = "[x]" if "[x]" in current else "[ ]"

        match = re.search(r"\[(\d)\]", current)
        if match:
            priority = f"[{match.group(1)}]"
        else:
            priority = "[2]"

        tasks[index] = f"{status} {priority} {new_text}\n"
        write_tasks(tasks)
        return True
    else:
        return False

#отметка задач как выполненная/ невыполненная
# [ ] — задача не выполнена
# [x] — задача выполнена
def toggle_task_status(index, complete = True):
    tasks = read_tasks()
    if 0 <= index < len(tasks):
        current = tasks[index].strip()

        if complete:
            if current.startswith('[ ]'):
                tasks[index] = current.replace('[ ]', '[x]', 1) + '\n'
                write_tasks(tasks)
                return 'marked_done'
            elif current.startswith('[x]'):
                return 'already_done'

        else:
            if current.startswith('[x]'):
                tasks[index] = current.replace('[x]', '[ ]', 1) + '\n'
                write_tasks(tasks)
                return 'marked_undone'
            elif current.startswith('[ ]'):
                return 'already_undone'

    return 'invalid_index'

#сортировка задач на выполненные/ невыполненные
def sort_tasks():
    tasks = read_tasks()

    completed = [task for task in tasks if task.strip().startswith('[x] ')]
    incomplete = [task for task in tasks if task.strip().startswith('[ ] ')]

    other = [task for task in tasks if task not in completed and task not in incomplete]

    sorted_tasks = incomplete + completed + other
    write_tasks(sorted_tasks)

    print("Задачи отсортированы: невыполненные сначала, выполненные — после.")

#Поиск задач по ключевому слову
def search_tasks(query):
    tasks = read_tasks()
    result = []
    for task in tasks:
        if query.lower() in task[3:].lower():
            result.append(task.strip())
    return result

# Экспорт задач в .txt файл под выбранным именем
def export_tasks(filename):
    tasks = read_tasks()
    with open(filename, "w", encoding="utf-8") as file:
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Экспорт задач - {current_date}\n")
        file.write("=" * 40 + "\n")
        for task in tasks:
            file.write(task.strip() + '\n')

# Импорт задач из другого файла и добавление в текущий
def import_tasks(filename):
    current_tasks = read_tasks()

    try:
        with open(filename, 'r', encoding="utf-8") as file:
            new_tasks = file.readlines()
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        return
    clean_new_tasks = [task.strip() for task in new_tasks if task.strip()]
    formatted_new_tasks = [f"[ ] {task}\n" for task in clean_new_tasks]

    update_tasks = current_tasks + formatted_new_tasks

    write_tasks(update_tasks)

    print(f"Добавлено {len(formatted_new_tasks)} задач(и) из файла '{filename}'")
