from telegram import Update
from telegram.ext import ContextTypes
from core import load_tasks, save_tasks, get_task_list

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Пожалуйста, укажите номер задачи для удаления. Например: /delete 2")
        return

    index = int(context.args[0]) - 1
    tasks = load_tasks()

    if 0 <= index < len(tasks):
        deleted_task = tasks.pop(index)
        save_tasks(tasks)
        await update.message.reply_text(f"Удалена задача № {index + 1} {deleted_task['title']}")
        message = get_task_list(tasks)
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(f"Задачи с номером {index + 1} нет в списке.")
