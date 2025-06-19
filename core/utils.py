from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_markup():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📋 Отобразить список задач", callback_data="list"),
        ],
        [
            InlineKeyboardButton("⚙ Настройки", callback_data="settings"),
        ]
    ])

def list_menu_markup():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📋 Действия с задачами", callback_data="listinline"),
        ],
    ])
