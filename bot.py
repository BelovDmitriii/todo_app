from telegram import Update
from dotenv import load_dotenv
import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from tasks import load_tasks, save_tasks

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой ToDo-бот.\n"
        "Используй команду /list, чтобы посмотреть задачи.\n"
        "И команду /add, чтобы добавить новую задачу."
    )

async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks:
        await update.message.reply_text("У вас пока нет задач ✅")
    else:
        message = "Ваши задачи:\n\n"
        for i,task in enumerate(tasks, start=1):
            status = "✅" if task.get("done") else "🔲"
            message += f"{i}. {status} {task['title']} (Приоритет: {task['priority']})\n\n"
        await update.message.reply_text(message)

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

    await update.message.reply_text(f"Добавлена задача: {title}")

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Пожалуйста, укажите номер задачи для удаления. Например: /delete 2")
        return

    index = int(context.args[0]) - 1
    tasks = load_tasks()

    if 0 <= index < len(tasks):
        deleted_task = tasks.pop(index)
        save_tasks(tasks)
        await update.message.reply_text(f"Удалена задача № {index + 1} {deleted_task["title"]}")
    else:
        await update.message.reply_text(f"Задачи с номером {index + 1} нет в списке.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list))
    app.add_handler(CommandHandler("delete", delete_task))
    app.run_polling()
