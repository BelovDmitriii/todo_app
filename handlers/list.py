from telegram import Update
from telegram.ext import ContextTypes
from core import load_tasks, get_task_list


async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    message = get_task_list(tasks)
    await update.message.reply_text(message)
