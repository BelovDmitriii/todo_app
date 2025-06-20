from config import TOKEN
from handlers import register_handlers
from telegram.ext import ApplicationBuilder
from core.db import init_db

init_db()

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    register_handlers(app)
    app.run_polling()
