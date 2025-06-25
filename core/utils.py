from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_markup():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Добавить задачу", callback_data="add"),
            InlineKeyboardButton("🧹 Очистить задачи", callback_data="clear"),
        ],
        [
            InlineKeyboardButton("📋 Отобразить список задач", callback_data="list"),
            InlineKeyboardButton("❓ Помощь", callback_data="help"),
        ],
    ])

def list_menu_markup():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Добавить задачу", callback_data="add"),
            InlineKeyboardButton("🧹 Очистить задачи", callback_data="clear"),
        ],
        [
            InlineKeyboardButton("📋 Действия с задачами", callback_data="listinline"),
            InlineKeyboardButton("❓ Помощь", callback_data="help"),
        ],
        [
            InlineKeyboardButton("🔀 Отсортировать задачи", callback_data="sort"),
        ],
    ])

def short_list_menu_markup():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Добавить задачу", callback_data="add"),
            InlineKeyboardButton("📋 Отобразить список задач", callback_data="list"),
        ],
        [
            InlineKeyboardButton("❓ Помощь", callback_data="help"),
        ],
    ])

def get_task_list(tasks: list) -> str:
    if not tasks:
        return "У вас пока нет задач ✅"

    message = "📋 Ваши задачи:\n\n"
    for i, task in enumerate(tasks, start=1):
        status = "✅" if task.done else "🔲"
        priority_icon = {3: "🔥", 2: "⚠️", 1: "📝"}.get(task.priority, "")
        message += f"{i}. {status} {priority_icon} {task.title}\n\n"

    return message

def confirm_clear_marcup():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Да", callback_data="confirm_clear"),
            InlineKeyboardButton("❌ Нет", callback_data="cancel_clear"),
        ]
    ])
