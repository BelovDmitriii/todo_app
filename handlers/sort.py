from telegram import Update
from telegram.ext import ContextTypes
from core.db import get_tasks
from core.db import sort_tasks_by_status
from core.utils import get_task_list

async def sort_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_tasks()
    if not tasks:
        await update.message.reply_text("У вас пока нет задач ✅")
        return

    sorted_tasks = sort_tasks_by_status()

    if not sorted_tasks:
        await update.message.reply_text("📭 У вас пока нет задач.")
        return

    message = get_task_list(sorted_tasks)
    await update.message.reply_text(f"📋 Задачи отсортированы:\n\n{message}")
