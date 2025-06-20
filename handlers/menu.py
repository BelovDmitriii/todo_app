# from telegram import Update
# from telegram.ext import ContextTypes

# from core.tasks_old import load_tasks, save_tasks, Task
# from core.utils import main_menu_markup

# async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     action = context.user_data.get("action")

#     if action == "add_task":
#         tasks = load_tasks()
#         new_task = Task(title=text, done=False, priority=2)
#         tasks.append(new_task)
#         save_tasks(tasks)

#         await update.message.reply_text(
#             f"✅ Задача добавлена: {text}",
#             reply_markup=main_menu_markup()
#         )
#         context.user_data["action"] = None
#         return
