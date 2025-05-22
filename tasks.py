# отображение задач в консоли
def list_tasks():
    tasks = read_tasks()
    if not tasks:
        print("Список задач пуст.")
        return

    print("Текущие задачи:")
    for i, task in enumerate(tasks):
        task = task.strip()
        if task.startswith('[x]'):
            display_task = task.replace('[x]', '✅', 1)
        elif task.startswith('[ ]'):
            display_task = task.replace('[ ]', '🔲', 1 )
        else:
            display_task = task
        print(f"{i + 1}. {display_task.strip()}")

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
