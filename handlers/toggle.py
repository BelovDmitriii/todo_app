from telegram import Update
from telegram.ext import ContextTypes
from core import load_tasks, save_tasks, get_task_list

async def toggle_task_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(f"Пожалуйста, укажите номер задачи для переключения статуса. Например: /done 1")
        return

    index = int(context.args[0]) - 1
    tasks = load_tasks()

    if 0 <= index < len(tasks):
        tasks[index]["done"] = not tasks[index].get("done", False)
        save_tasks(tasks)
        status = "выполнена" if tasks[index]["done"] else "не выполнена"

        await update.message.reply_text(f"Статус задачи изменён: {tasks[index]['title']} — {status}")
        message = get_task_list(tasks)
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Некорректный номер задачи.")
