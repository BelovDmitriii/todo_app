from telegram import Update
from telegram.ext import ContextTypes
from emojis import EMOJIS

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == EMOJIS['buttons']['list']:
        await update.message.reply_text("Вот твои задачи...")

    elif text == EMOJIS['buttons']['add']:
        await update.message.reply_text("Введите задачу, которую хотите добавить:")
        context.user_data["action"] = "add_task"

    elif text == EMOJIS['buttons']['delete']:
        await update.message.reply_text("Введите номер задачи для удаления:")
        context.user_data["action"] = "delete_task"

    elif text == EMOJIS['buttons']['settings']:
        await update.message.reply_text("Тут будут настройки (в будущем).")

    else:
        action = context.user_data.get("action")
        if action == "add_task":
            await update.message.reply_text(f"Задача '{text}' добавлена!")
            context.user_data["action"] = None

        elif action == "delete_task":
            await update.message.reply_text(f"Задача под номером '{text}' удалена!")
            context.user_data["action"] = None

        else:
            await update.message.reply_text("Выбери действие с помощью кнопок 👇")
