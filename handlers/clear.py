from telegram import Update
from telegram.ext import ContextTypes
from core.utils import confirm_clear_marcup

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вы уверены, что хотите удалить ВСЕ задачи?",
        reply_markup=confirm_clear_marcup()
    )
