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
