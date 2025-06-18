from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

main_menu_keyboard = [
    ["➕ Добавить", "📋 Список"],
    ["🗑 Удалить", "⚙ Настройки"]
]

main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой ToDo-бот.\n"
        "Используй команду /list, чтобы посмотреть задачи.\n"
        "И команду /help, чтобы посмотреть все возможные команды.",
        reply_markup=main_menu_markup
    )
