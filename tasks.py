def add_task(task_text, filename = 'tasks.txt'):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(task_text + '\n')

def read_tasks(filename = 'tasks.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []
