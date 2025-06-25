from telegram import Update
from telegram.ext import ContextTypes

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
        "/clear - удалить все задачи\n"
    )
    msg = update.message or update.callback_query.message
    await msg.reply_text(help_text, parse_mode="Markdown")
