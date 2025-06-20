from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.db import get_tasks, toggle_task_done, delete_task_by_index, clear_all_tasks, sort_tasks_by_priority
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

    await message_obj.reply_text("\ud83d\udccb *Ваши задачи:*", parse_mode="Markdown")

    for i, task in enumerate(tasks):
        status = "\u2705" if task.done else "\ud83d\udd32"
        priority_icon = {3: "\ud83d\udd25", 2: "\u26a0\ufe0f", 1: "\ud83d\udcdd"}.get(task.priority, "")
        message = f"*{i + 1}. {status} {priority_icon} {task.title}*"

        task_buttons = [
            InlineKeyboardButton("\u2705 Выполнить/Отменить", callback_data=f"toggle_{task.id}"),
            InlineKeyboardButton("\ud83d\uddd1 Удалить", callback_data=f"delete_{task.id}"),
            InlineKeyboardButton("\u270f\ufe0f Изменить", callback_data=f"edit_{task.id}")
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
        await query.edit_message_text(message, reply_markup=list_menu_markup(), parse_mode="Markdown")

    elif data == "listinline":
        await query.delete_message()
        await list_with_inline(update, context)

    elif data == "help":
        await help_command(update, context)

    elif data == "add":
        await ask_add_task(update, context)

    elif data == "clear":
        clear_all_tasks()
        await query.edit_message_text("\ud83e\ude9d Все задачи успешно удалены.", reply_markup=list_menu_markup())

    elif data == "sort":
        tasks = sort_tasks_by_priority()
        message = get_task_list(tasks)
        await query.edit_message_text(message, reply_markup=list_menu_markup(), parse_mode="Markdown")

    elif data.startswith("toggle_"):
        task_id = int(data.split("_")[1])
        toggle_task_done(task_id)
        task = next((t for t in get_tasks() if t.id == task_id), None)
        if task:
            await query.edit_message_text(f"Статус задачи изменён: {task.title}")
        else:
            await query.edit_message_text("Задача не найдена.")

    elif data.startswith("delete_"):
        task_id = int(data.split("_")[1])
        task = delete_task_by_index(task_id)
        if task:
            await query.edit_message_text(f"Удалена задача: {task.title}")
        else:
            await query.edit_message_text("Неверный ID задачи.")

    elif data.startswith("edit_"):
        task_id = int(data.split("_")[1])
        context.user_data["edit_id"] = task_id
        task = next((t for t in get_tasks() if t.id == task_id), None)
        if task:
            await query.edit_message_text(f"Введите новый текст для задачи:\n\n*{task.title}*", parse_mode="Markdown")
        else:
            await query.edit_message_text("Задача не найдена.")

    else:
        tasks = get_tasks()
        message = get_task_list(tasks)
        await query.edit_message_text(message)
