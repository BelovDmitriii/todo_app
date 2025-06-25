from telegram import Update
from telegram.ext import ContextTypes
from core.utils import get_task_list
from core.db import get_tasks, delete_task_by_id
from core.utils import list_menu_markup

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Пожалуйста, укажите номер задачи для удаления. Например: /delete 2")
        return

    index = int(context.args[0]) - 1
    tasks = get_tasks()

    if 0 <= index < len(tasks):
        task = tasks[index]
        delete_task_by_id(task.id)
        await update.message.reply_text(f"Удалена задача № {index + 1} {task.title}")

        updated_tasks = get_tasks()
        message = get_task_list(updated_tasks)
        await update.message.reply_text(message,reply_markup=list_menu_markup())
    else:
        await update.message.reply_text(f"Задачи с номером {index + 1} нет в списке.")
