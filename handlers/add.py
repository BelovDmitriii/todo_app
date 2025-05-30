from telegram import Update
from telegram.ext import ContextTypes
from core import load_tasks, save_tasks, get_task_list
from emojis import EMOJIS

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажите текст задачи после команды /add.")
        return

    *title_parts, last = context.args

    priority = 2

    if last.isdigit() and int(last) in (1, 2, 3):
        priority = int(last)
        title = " ".join(title_parts)
    else:
        title = " ".join(context.args)

    new_task = {
        "title": title,
        "priority": priority,
        "done": False
    }

    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)

    await update.message.reply_text(f"Добавлена задача: {title}{EMOJIS['status']['done']}")
    message = get_task_list(tasks)
    await update.message.reply_text(message)
