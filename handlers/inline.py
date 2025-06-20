import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.db import get_tasks, clear_all_tasks, sort_tasks_by_status, toggle_task_done, delete_task_by_index
from core.utils import list_menu_markup, main_menu_markup, get_task_list
from .help import help_command
from handlers.add import ask_add_task
from emojis import EMOJIS

async def list_with_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_tasks()

    message_obj = update.message or update.callback_query.message

    if not tasks:
        await message_obj.reply_text(f"Список задач пуст. {EMOJIS['status']['cancelled']}", reply_markup=main_menu_markup())
        return

    await message_obj.reply_text("📋 *Ваши задачи:*", parse_mode="Markdown")

    for i, task in enumerate(tasks):
        status = "✅" if task.done else "🔲"
        priority_icon = {3: "🔥", 2: "⚠️", 1: "📝"}.get(task.priority, "")
        message = f"*{i + 1}. {status} {priority_icon} {task.title}*"

        task_buttons = [
            InlineKeyboardButton("✅ Выполнить/Отменить", callback_data=f"toggle_{i}"),
            InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_{i}"),
            InlineKeyboardButton("✏️ Изменить", callback_data=f"edit_{i}")
        ]
        keyboard = InlineKeyboardMarkup([task_buttons])

        await message_obj.reply_text(message, reply_markup=keyboard, parse_mode="Markdown")

    await message_obj.reply_text("Ниже можно отобразить текущий список задач", reply_markup=main_menu_markup())

async def inline_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "list":
        tasks = get_tasks()
        message = get_task_list(tasks)
        await query.edit_message_text(message,reply_markup=list_menu_markup(), parse_mode="Markdown")

    elif data == "listinline":
        await query.delete_message()
        await list_with_inline(update, context)

    elif data == "help":
        await help_command(update, context)

    elif data == "add":
        await ask_add_task(update, context)

    elif data == "clear":
        if tasks:
            clear_all_tasks()
            await query.edit_message_text("🧹 Все задачи успешно удалены.", reply_markup=list_menu_markup())
        else:
            await query.edit_message_text("Список задач уже пуст.😕", reply_markup=list_menu_markup())

    elif data == "sort":
        sorted_tasks = sort_tasks_by_status()
        if not sorted_tasks:
            await query.edit_message_text("Список задач пока пуст.😕", reply_markup=list_menu_markup())
        else:
            message = get_task_list(sorted_tasks)
            try:
                await query.edit_message_text(message, reply_markup=list_menu_markup(), parse_mode="Markdown")
            except telegram.error.BadRequest as e:
                if "Message is not modified" in str(e):
                    pass
                else:
                    raise

    elif data.startswith("toggle_"):
        index = int(data.split("_")[1])
        toggle_task_done(index)
        task = next((t for t in get_tasks() if t.id == index), None)
        if task:
            await query.edit_message_text(f"Статус задачи изменён: {task.title}")
        else:
            await query.edit_message_text("Задача не найдена.")

    elif data.startswith("delete_"):
        index = int(data.split("_")[1])
        task = delete_task_by_index(index)
        if task:
            await query.edit_message_text(f"Удалена задача: {task.title}")
        else:
            await query.edit_message_text("Неверный индекс задачи.")

    elif data.startswith("edit_"):
        index = int(data.split("_")[1])
        context.user_data["edit_id"] = index
        task = next((t for t in get_tasks() if t.id == index), None)
        if task:
            await query.edit_message_text(f"Введите новый текст для задачи:\n\n*{tasks[index].title}*", parse_mode="Markdown")
        else:
            await query.edit_message_text("Задача не найдена.")

    else:
        tasks = get_tasks()
        message = get_task_list(tasks)
        await query.edit_message_text(message)
