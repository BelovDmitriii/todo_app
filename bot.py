from config import TOKEN
from handlers import register_handlers
from telegram.ext import ApplicationBuilder

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    register_handlers(app)
    app.run_polling()
