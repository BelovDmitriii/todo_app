from telegram import Update
from telegram.ext import ContextTypes
from core.utils import get_task_list
from core.db import get_tasks, SessionLocal
from core.utils import short_list_menu_markup
from core.models import Task

async def edit_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2 or not context.args[0].isdigit():
        await update.message.reply_text("Использование: /edit <номер> <новый текст задачи>")
        return

    index = int(context.args[0]) - 1
    new_title = " ".join(context.args[1:])
    tasks = get_tasks()

    if 0 <= index < len(tasks):
        old_title = tasks[index]["title"]
        tasks[index]["title"] = new_title
        await update.message.reply_text(f"Задача изменена:\n{old_title} → {new_title}")
        message = get_task_list(tasks)
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Некорректный номер задачи.")

async def handle_edit_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "edit_id" not in context.user_data:
        await update.message.reply_text("Не удалось определить задачу для редактирования.")
        return

    new_text = update.message.text.strip()
    task_id = context.user_data.pop("edit_id")
    session = SessionLocal()

    task = session.get(Task, task_id)
    if task:
        old_title = task.title
        task.title = new_text
        session.commit()
        await update.message.reply_text(f"✅ Задача обновлена:\n\n{old_title} → {new_text}", reply_markup=short_list_menu_markup())
    else:
        await update.message.reply_text("Задача не найдена.")
    session.close()
