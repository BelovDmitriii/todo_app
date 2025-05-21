import sys

# print("Аргументы командной строки:", sys.argv)

from tasks import add_task, read_tasks

def main():
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
    else:
        print(f"Неизвестная команда: {command}")

if __name__ == '__main__':
    main()
