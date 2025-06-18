from telegram import Update
from telegram.ext import ContextTypes

from .edit import handle_edit_reply
from .menu import handle_main_menu

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    action = context.user_data.get("action")

    if action == "edit_task":
        await handle_edit_reply(update, context)
    else:
        await handle_main_menu(update, context)
