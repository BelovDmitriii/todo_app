from telegram import Update
from telegram.ext import ContextTypes
from core import load_tasks, save_tasks, get_task_list

async def edit_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2 or not context.args[0].isdigit():
        await update.message.reply_text("Использование: /edit <номер> <новый текст задачи>")
        return

    index = int(context.args[0]) - 1
    new_title = " ".join(context.args[1:])
    tasks = load_tasks()

    if 0 <= index < len(tasks):
        old_title = tasks[index]["title"]
        tasks[index]["title"] = new_title
        save_tasks(tasks)
        await update.message.reply_text(f"Задача изменена:\n{old_title} → {new_title}")
        message = get_task_list(tasks)
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Некорректный номер задачи.")

async def handle_edit_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "edit_index" not in context.user_data:
        return

    new_text = update.message.text.strip()
    index = context.user_data.pop("edit_index")

    tasks = load_tasks()
    if 0 <= index < len(tasks):
        old_title = tasks[index]["title"]
        tasks[index]["title"] = new_text
        save_tasks(tasks)
        await update.message.reply_text(f"✅ Задача обновлена:\n\n{old_title} → {new_text}")
    else:
        await update.message.reply_text("Задача не найдена.")
