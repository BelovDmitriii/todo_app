from telegram import Update
from telegram.ext import ContextTypes
from core.db import get_tasks
from core import get_task_list
from core.utils import list_menu_markup

async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_tasks()
    if not tasks:
        await update.message.reply_text("Список задач пуст 😕", reply_markup=list_menu_markup())
        return

    message = get_task_list(tasks)
    await update.message.reply_text(message, reply_markup=list_menu_markup())
