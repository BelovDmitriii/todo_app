from telegram import Update
from dotenv import load_dotenv
import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from tasks import load_tasks

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks:
        await update.message.reply_text("У вас пока нет задач ✅")
    else:
        message = "Ваши задачи:\n\n"
        for task in tasks:
            status = "✅" if task.get("done") else "🔲"
            message += f"{status} {task['title']} (Приоритет: {task['priority']})\n"
        await update.message.reply_text(message)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
