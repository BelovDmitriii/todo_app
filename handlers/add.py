from telegram import Update
from telegram.ext import ContextTypes
from core import load_tasks, save_tasks, get_task_list
from emojis import EMOJIS

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title = " ".join(context.args)
    if not title:
        await update.message.reply_text("Пожалуйста, укажите текст задачи после команды /add.")
        return

    new_task = {
        "title": title,
        "priority": 2,
        "done": False
    }

    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)

    await update.message.reply_text(f"Добавлена задача: {title}{EMOJIS['status']['done']}")
    message = get_task_list(tasks)
    await update.message.reply_text(message)
