from .start import start
from .add import add
from .list import list
from .delete import delete_task
from .help import help_command
from .edit import edit_task
from .text_message import text_message_handler
from .toggle import toggle_task_status
from .sort import sort_command
from .search import search_tasks
from .inline import list_with_inline, inline_callback_handler
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters

def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("delete", delete_task))
    app.add_handler(CommandHandler("edit", edit_task))
    app.add_handler(CommandHandler("done", toggle_task_status))
    app.add_handler(CommandHandler("sort", sort_command))
    app.add_handler(CommandHandler("search", search_tasks))
    app.add_handler(CommandHandler("listinline", list_with_inline))
    app.add_handler(CallbackQueryHandler(inline_callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))

    app.run_polling()
