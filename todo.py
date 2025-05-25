from tasks import add_task, load_tasks, save_tasks, edit_task, toggle_task_status, list_tasks, sort_tasks, search_tasks, export_tasks, import_tasks
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
            return

        task_text = ' '.join(sys.argv[2:-1])

        try:
            priority = int(sys.argv[-1])
            if priority not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            task_text = ' '.join(sys.argv[2:])
            priority = 2

        add_task(task_text, priority)
        print(f"Задача добавлена с приоритетом {priority}: {task_text}")

    elif command == 'list':
        list_tasks()

    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Укажите хотя бы один номер задачи для удаления. Например: delete 2 4")
        else:
            task_numbers = sys.argv[2:]

            if not all(num.isdigit() for num in task_numbers):
                print("Все номера задач должны быть числами. Например: delete 1 3 5")
            else:
                tasks = load_tasks()

                if not tasks:
                    print("Список задач пуст, нечего удалять.")
                    return
                indexes = sorted(set(int(n) - 1 for n in task_numbers), reverse=True)

                removed_tasks = []

                for idx in indexes:
                    if 0 <= idx < len(tasks):
                        removed_tasks.append(tasks.pop(idx))
                    else:
                        print(f"Нет задачи с номером: {idx + 1}")

                save_tasks(tasks)

                if removed_tasks:
                    print("Удалены задачи:")
                    for task in removed_tasks:
                        print(f" - {task}")

    elif command == 'edit':
        if len(sys.argv) < 4 or not sys.argv[2].isdigit():
            print("Использование: python todo.py edit <номер> \"новый текст задачи\"")
        else:
            index = int(sys.argv[2]) - 1
            new_text = ' '.join(sys.argv[3:])

            tasks = load_tasks()

            if edit_task(index, new_text):
                print(f"Задача {index + 1} изменена на: {new_text}")
            else:
                print("Некорректный номер задачи")

    elif command == 'complete':

        if len(sys.argv) < 3:
            print("Укажите номер задачи.")
            return
        try:
            index = int(sys.argv[2]) - 1
        except ValueError:
            print("Введите корректный номер.")
            return
        result = toggle_task_status(index, complete=True)

        if result == 'marked_done':
            print(f"Задача №{index + 1} отмечена как выполненная.")
        elif result == 'already_done':
            print("Задача уже отмечена как выполненная.")
        elif result == 'invalid_index':
            print("Некорректный номер задачи.")

    elif command == 'incomplete':
        if len(sys.argv) < 3:
            print("Укажите номер задачи.")
            return
        try:
            index = int(sys.argv[2]) - 1
        except ValueError:
            print("Введите корректный номер.")
            return
        result = toggle_task_status(index, complete=False)

        if result == 'marked_undone':
            print(f"Задача №{index + 1} отмечена как невыполненная.")
        elif result == 'already_undone':
            print("Задача уже отмечена как невыполненная.")
        elif result == 'invalid_index':
            print("Некорректный номер задачи.")

    elif command == 'sort':
        sort_tasks()

    elif command == 'search':

        if len(sys.argv) < 3:
            print("Укажите слово, которое надо найти в задаче.")
            return

        query = ' '.join(sys.argv[2:])
        found = search_tasks(query)

        if found:
            print(f"Результат поиска по запросу '{query}': ")
            for i, task in enumerate(found, 1):
                print(f"{i}. {task.strip()}")
        else:
            print(f"По запросу '{query}' ничего не найдено.")

    elif command == 'export':

        if len(sys.argv) < 3:
            print("Необходимо указать имя файла.")
            return

        filename = ' '.join(sys.argv[2:])

        if not filename.endswith('.txt'):
            filename += '.txt'

        export_tasks(filename)
        print(f"Задачи экспортированы в файл '{filename}'")

    elif command == 'import':
        if len(sys.argv) < 3:
            print("Необходимо указать имя файла, из которого планируется перенести задачи.")
            return

        filename = ' '.join(sys.argv[2:])

        if not filename.endswith('.txt'):
            filename += '.txt'

        import_tasks(filename)

    else:
        print(f"Неизвестная команда: {command}")

if __name__ == '__main__':
    main()
