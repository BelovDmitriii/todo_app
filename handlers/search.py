from telegram import Update
from telegram.ext import ContextTypes
from core import load_tasks

async def search_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args).lower()
    if not query:
        await update.message.reply_text("Пожалуйста, укажите слово для поиска. Например: /search отчет")
        return

    tasks = load_tasks()
    filtered = [task for task in tasks if query in task["title"].lower()]

    if not filtered:
        await update.message.reply_text(f"По запросу '{query}' задачи не найдены.")
        return

    message = f"Результаты поиска по '{query}':\n\n"
    for i, task in enumerate(filtered, 1):
        status = "✅" if task.get("done") else "🔲"
        priority_icon = {3: "🔥", 2: "⚠️", 1: "📝"}.get(task["priority"], "")
        message += f"{i}. {status} {priority_icon} {task['title']}\n\n"

    await update.message.reply_text(message)
