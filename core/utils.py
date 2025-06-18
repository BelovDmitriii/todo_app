from telegram import ReplyKeyboardMarkup

main_menu_keyboard = [
    ["➕ Добавить", "📋 Список"],
    ["🗑 Удалить", "⚙ Настройки"]
]

main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)
