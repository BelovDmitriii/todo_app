from telegram import Update
from telegram.ext import ContextTypes
from core.utils import get_task_list
from core.db import get_tasks, toggle_task_done
from core.utils import short_list_menu_markup

async def toggle_task_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(f"Пожалуйста, укажите номер задачи для переключения статуса. Например: /done 1")
        return

    index = int(context.args[0]) - 1
    tasks = get_tasks()

    if 0 <= index < len(tasks):
        task = tasks[index]
        toggle_task_done(task.id)

        updated_tasks = get_tasks()
        new_task = next((t for t in updated_tasks if t.id == task.id), None)
        status = "выполнена" if new_task and new_task.done else "не выполнена"

        await update.message.reply_text(f"Статус задачи изменён: {task.title} — {status}")
        message = get_task_list(updated_tasks)
        await update.message.reply_text(message, reply_markup=short_list_menu_markup())
    else:
        await update.message.reply_text("Некорректный номер задачи.")
