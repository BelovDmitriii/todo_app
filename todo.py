from tasks import add_task, read_tasks, write_tasks
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

    elif command == 'delete':
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Укажите номер задачи для удаления. Например: delete 2")
        else:
            task_number = int(sys.argv[2])
            tasks = read_tasks()
            if 1 <= task_number <= len(tasks):
                removed = tasks.pop(task_number - 1)
                write_tasks(tasks)
                print(f"Задача удалена: {removed}")
            else:
                print("Некорректный номер задачи.")

    else:
        print(f"Неизвестная команда: {command}")

if __name__ == '__main__':
    main()
