from tasks import add_task, read_tasks, write_tasks, edit_task, toggle_task_status
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
        if len(sys.argv) < 3:
            print("Укажите хотя бы один номер задачи для удаления. Например: delete 2 4")
        else:
            task_numbers = sys.argv[2:]

            if not all(num.isdigit() for num in task_numbers):
                print("Все номера задач должны быть числами. Например: delete 1 3 5")
            else:
                tasks = read_tasks()

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

                write_tasks(tasks)

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

            tasks = read_tasks()

            if edit_task(index, new_text):
                print(f"Задача {index + 1} изменена на: {new_text}")
            else:
                print("Некорректный номер задачи")

    elif command == 'complete':

        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Укажите номер задачи для завершения. Например: complete 2")
        else:
            index = int(sys.argv[2]) - 1

            if toggle_task_status(index, complete=True):
                print(f"Задача №{index + 1} отмечена как выполненная.")
            else:
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

        if toggle_task_status(index, complete=False):
            print(f"Задача №{index + 1} отмечена как невыполненная.")
        else:
            print("Некорректный номер задачи.")

        # if len(sys.argv) < 3 or not sys.argv[2].isdigit():
        #     print("Укажите номер задачи для снятия отметки. Например: incomplete 2")
        # else:
        #     index = int(sys.argv[2]) - 1

        #     if toggle_task_status(index, complete=False):
        #         print(f"Задача №{index + 1} отмечена как невыполненная.")
        #     else:
        #         print("Некорректный номер задачи.")

    else:
        print(f"Неизвестная команда: {command}")

if __name__ == '__main__':
    main()
