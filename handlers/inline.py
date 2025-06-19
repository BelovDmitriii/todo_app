from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core import load_tasks, save_tasks, get_task_list
from core.utils import list_menu_markup, main_menu_markup
from emojis import EMOJIS

async def list_with_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()

    message_obj = update.message or update.callback_query.message

    if not tasks:
        await message_obj.reply_text(f"Список задач пуст. {EMOJIS['status']['cancelled']}")
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
    tasks = load_tasks()

    if data == "list":
        message = get_task_list(tasks)
        await query.edit_message_text(message,reply_markup=list_menu_markup(), parse_mode="Markdown")

    elif data == "listinline":
        await query.delete_message()
        await list_with_inline(update, context)

    elif data.startswith("toggle_"):
        index = int(data.split("_")[1])
        if 0 <= index < len(tasks):
            task = tasks[index]
            task.done = not task.done
            save_tasks(tasks)
            await query.edit_message_text(f"Статус задачи изменён: {task.title}")
        else:
            await query.edit_message_text("Неверный индекс задачи.")

    elif data.startswith("delete_"):
        index = int(data.split("_")[1])
        if 0 <= index < len(tasks):
            deleted_task = tasks.pop(index)
            save_tasks(tasks)
            await query.edit_message_text(f"Удалена задача: {deleted_task.title}")
        else:
            await query.edit_message_text("Неверный индекс задачи.")

    elif data.startswith("edit_"):
        index = int(data.split("_")[1])
        if 0 <= index < len(tasks):
            context.user_data["edit_index"] = index
            await query.edit_message_text(f"Введите новый текст для задачи:\n\n*{tasks[index].title}*", parse_mode="Markdown")
        else:
            await query.edit_message_text("Неверный индекс задачи.")

    else:
        message = get_task_list(tasks)
        await query.edit_message_text(message)
