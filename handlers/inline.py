from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core import load_tasks, save_tasks, get_task_list
from emojis import EMOJIS

async def list_with_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks:
        await update.message.reply_text(f"Список задач пуст. {EMOJIS['status']['cancelled']}")
        return

    await update.message.reply_text("📋 *Ваши задачи:*", parse_mode="Markdown")

    for i, task in enumerate(tasks):
        status = "✅" if task.get("done") else "🔲"
        priority_icon = {3: "🔥", 2: "⚠️", 1: "📝"}.get(task["priority"], "")
        message = f"*{i + 1}. {status} {priority_icon} {task['title']}*"

        task_buttons = [
            InlineKeyboardButton("✅ Выполнить/Отменить", callback_data=f"toggle_{i}"),
            InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_{i}")
        ]
        keyboard = InlineKeyboardMarkup([task_buttons])

        await update.message.reply_text(message, reply_markup=keyboard, parse_mode="Markdown")


async def inline_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    tasks = load_tasks()

    if data.startswith("toggle_"):
        index = int(data.split("_")[1])
        if 0 <= index < len(tasks):
            tasks[index]["done"] = not tasks[index].get("done", False)
            save_tasks(tasks)
            await query.edit_message_text(f"Статус задачи изменён: {tasks[index]['title']}")
        else:
            await query.edit_message_text("Неверный индекс задачи.")

    elif data.startswith("delete_"):
        index = int(data.split("_")[1])
        if 0 <= index < len(tasks):
            deleted_task = tasks.pop(index)
            save_tasks(tasks)
            await query.edit_message_text(f"Удалена задача: {deleted_task['title']}")
        else:
            await query.edit_message_text("Неверный индекс задачи.")

    else:
        message = get_task_list(tasks)
        await query.edit_message_text(message)
