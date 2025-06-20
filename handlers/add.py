from telegram import Update
from telegram.ext import ContextTypes
from core.db import get_tasks, add_task
from core import get_task_list
from core.models import Task
from emojis import EMOJIS
from core.utils import main_menu_markup, short_list_menu_markup

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

    tasks = get_tasks()
    if any(task.title.lower() == title.lower() for task in tasks):
        await update.message.reply_text("⚠️ Такая задача уже есть в твоем списке.", reply_markup=short_list_menu_markup())
        return

    add_task(title=title, priority=priority)

    await update.message.reply_text(f"Добавлена задача: {title}{EMOJIS['status']['done']}")
    message = get_task_list(tasks)
    await update.message.reply_text(message, reply_markup=main_menu_markup())

async def ask_add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["action"] = "add"
    await update.callback_query.message.reply_text("📝 Введите текст новой задачи:")

async def handle_add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("action") != "add":
        await update.message.reply_text("⚠️ Введите команду или нажми одну из кнопок 👇", reply_markup=main_menu_markup())
        return

    title = update.message.text.strip()
    if not title:
        await update.message.reply_text("⚠️ Текст задачи не может быть пустым.")
        return

    tasks = get_tasks()

    if any(task.title.lower() == title.lower() for task in tasks):
        await update.message.reply_text("⚠️ Такая задача уже есть в твоем списке.", reply_markup=short_list_menu_markup())
        return

    add_task(title=title, priority=2)

    await update.message.reply_text(
        f"✅ Задача добавлена: {title}",
        reply_markup=main_menu_markup()
    )

    context.user_data["action"] = None
