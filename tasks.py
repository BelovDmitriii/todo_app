from datetime import datetime

def get_status_symbol(task):
    if task.startswith('[x]'):
        return '✅'
    elif task.startswith('[ ]'):
        return '🔲'
    else:
        return ''

# отображение задач в консоли
def list_tasks():
    tasks = read_tasks()
    if not tasks:
        print("Список задач пуст.")
        return

    print("Текущие задачи:")
    for i, task in enumerate(tasks, start=1):
        status = get_status_symbol(task)
        text = task[4:].strip()
        print(f"{i}. {status} {text}")

#добавление задачи
def add_task(task_text, filename = 'tasks.txt'):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"[ ] {task_text}\n")

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
        tasks[index] = new_text
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
