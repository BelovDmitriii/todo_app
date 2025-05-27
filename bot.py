from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from tasks import load_tasks, save_tasks, get_task_list, sort_tasks
from emojis import EMOJIS

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой ToDo-бот.\n"
        "Используй команду /list, чтобы посмотреть задачи.\n"
        "И команду /help, чтобы посмотреть все возможные команды."
    )

async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    message = get_task_list(tasks)
    await update.message.reply_text(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 *Доступные команды:*\n\n"
        "/start — приветствие и краткая инструкция\n"
        "/help — показать это сообщение\n"
        "/add <текст задачи> — добавить новую задачу, далее через пробел приоритет\n"
        "/list — показать текущие задачи\n"
        "/delete <номер> — удалить задачу\n"
        "/edit <номер> <новый текст> — изменить задачу\n"
        "/done <номер> — отметить задачу выполненной / невыполненной\n"
        "/sort — отсортировать задачи по приоритету и статусу\n"
        "/search <ключевое слово> — найти задачи по тексту\n"
        "/listinline - выводит задачи с инлайн-кнопками\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

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

    await update.message.reply_text(f"Добавлена задача: {title}{EMOJIS['status']['done']}")
    message = get_task_list(tasks)
    await update.message.reply_text(message)

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Пожалуйста, укажите номер задачи для удаления. Например: /delete 2")
        return

    index = int(context.args[0]) - 1
    tasks = load_tasks()

    if 0 <= index < len(tasks):
        deleted_task = tasks.pop(index)
        save_tasks(tasks)
        await update.message.reply_text(f"Удалена задача № {index + 1} {deleted_task['title']}")
        message = get_task_list(tasks)
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(f"Задачи с номером {index + 1} нет в списке.")

async def edit_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2 or not context.args[0].isdigit():
        await update.message.reply_text("Использование: /edit <номер> <новый текст задачи>")
        return

    index = int(context.args[0]) - 1
    new_title = " ".join(context.args[1:])
    tasks = load_tasks()

    if 0 <= index < len(tasks):
        old_title = tasks[index]["title"]
        tasks[index]["title"] = new_title
        save_tasks(tasks)
        await update.message.reply_text(f"Задача изменена:\n{old_title} → {new_title}")
        message = get_task_list(tasks)
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Некорректный номер задачи.")

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

async def sort_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks:
        await update.message.reply_text("У вас пока нет задач ✅")
        return

    sorted_tasks = sort_tasks(tasks)
    save_tasks(sorted_tasks)

    message = "📋 Задачи отсортированы:\n\n"
    for idx, task in enumerate(sorted_tasks, start=1):
        status = "✅" if task["done"] else "🔲"
        priority_icon = {3: "🔥", 2: "⚠️", 1: "📝"}.get(task["priority"], "")
        message += f"{idx}. {status} {priority_icon} {task['title']}\n\n"

    await update.message.reply_text(message)

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

async def list_with_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks:
        await update.message.reply_text(f"Список задач пуст. {EMOJIS['status']['cancelled']}")
        return

    for i, task in enumerate(tasks):
        status = "✅" if task.get("done") else "🔲"
        priority_icon = {3: "🔥", 2: "⚠️", 1: "📝"}.get(task["priority"], "")
        text = f"*{i + 1}. {status} {priority_icon} {task['title']}*"

        buttons = [
            InlineKeyboardButton("✅ Выполнить/Отменить", callback_data=f"toggle_{i}"),
            InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_{i}")
        ]

        reply_markup = InlineKeyboardMarkup([buttons])
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

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
        # Просто обновим список после любого действия
        message = get_task_list(tasks)
        await query.edit_message_text(message)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list))
    app.add_handler(CommandHandler("delete", delete_task))
    app.add_handler(CommandHandler("edit", edit_task))
    app.add_handler(CommandHandler("done", toggle_task_status))
    app.add_handler(CommandHandler("sort", sort_command))
    app.add_handler(CommandHandler("search", search_tasks))
    app.add_handler(CommandHandler("listinline", list_with_inline))
    app.add_handler(CallbackQueryHandler(inline_callback_handler))
    app.run_polling()
