from telegram import Update
from telegram.ext import ContextTypes
from core import load_tasks, save_tasks, sort_tasks

async def sort_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks:
        await update.message.reply_text("У вас пока нет задач ✅")
        return

    sorted_tasks = sort_tasks(tasks)
    save_tasks(sorted_tasks)

    message = "📋 Задачи отсортированы:\n\n"
    for idx, task in enumerate(sorted_tasks, start=1):
        status = "✅" if task["done"] else "🔲"
        priority_icon = {3: "🔥", 2: "⚠️", 1: "📝"}.get(task["priority"], "")
        message += f"{idx}. {status} {priority_icon} {task['title']}\n\n"

    await update.message.reply_text(message)
