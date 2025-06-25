from telegram import Update
from telegram.ext import ContextTypes
from core.db import get_tasks
from core.utils import short_list_menu_markup

async def search_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args).lower()
    if not query:
        await update.message.reply_text("Пожалуйста, укажите слово для поиска. Например: /search отчет")
        return

    tasks = get_tasks()
    filtered = [task for task in tasks if query in task.title.lower()]

    if not filtered:
        await update.message.reply_text(f"По запросу '{query}' задачи не найдены.", reply_markup=short_list_menu_markup())
        return

    message = f"Результаты поиска по '{query}':\n\n"
    for i, task in enumerate(filtered, 1):
        status = "✅" if task.done else "🔲"
        priority_icon = {3: "🔥", 2: "⚠️", 1: "📝"}.get(task.priority, "")
        message += f"{i}. {status} {priority_icon} {task.title}\n\n"

    await update.message.reply_text(message, reply_markup=short_list_menu_markup())
