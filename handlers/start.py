from telegram import Update
from telegram.ext import ContextTypes
from core.utils import main_menu_markup


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой ToDo-бот.\n"
        "Используй команду /list, чтобы посмотреть задачи.\n"
        "И команду /help, чтобы посмотреть все возможные команды.",
        reply_markup=main_menu_markup()
    )
