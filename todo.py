TASKS_FILE = 'tasks.txt'

def load_tasks():
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        for task in tasks:
            f.write(task + '\n')

def show_tasks(tasks):
    if not tasks:
        print('Список задач пуст')
    else:
        print('Текущие задачи:')
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

def add_task(tasks):
    new_task = input('Введите новую задачу: ')
    tasks.append(new_task)
    save_tasks(tasks)
    print('Задача добавлена!')

def main():
    tasks = load_tasks()

    while True:
        print('\n1. Показать задачи')
        print('2. Добавить задачу')
        print('3. Выйти')

        choice = input('Выберите действие: ')

        if choice == '1':
            show_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            break
        else:
            print('Неверный выбор. Попробуйте еще раз.')

if __name__ == '__main__':
    main()
