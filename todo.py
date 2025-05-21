from tasks import add_task, read_tasks
import sys

def main():
    # print("Аргументы командной строки:", sys.argv)

    if len(sys.argv) < 2:
        print("Использование: python todo.py add 'текст задачи'")
        return

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 3:
            print("Ошибка: не указан текст задачи.")
        else:
            task_text = ' '.join(sys.argv[2:])
            add_task(task_text)
            print(f"Задача добавлена: {task_text}")

    elif command == 'list':
        tasks = read_tasks()
        if not tasks:
            print("Список задач пуст.")
        else:
            print("Текущие задачи: ")
            for i, task in enumerate(tasks, start = 1):
                print(f"{i}. {task}")

    else:
        print(f"Неизвестная команда: {command}")

if __name__ == '__main__':
    main()
