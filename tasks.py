#добавление задачи
def add_task(task_text, filename = 'tasks.txt'):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(task_text + '\n')

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
            file.write(task + '\n')

#редактирование задачи в файле
def edit_task(index, new_text):
    tasks = read_tasks()
    if 0 <= index < len(tasks):
        tasks[index] = new_text
        write_tasks(tasks)
        return True
    else:
        return False
