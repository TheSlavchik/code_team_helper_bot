from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Мой профиль"), KeyboardButton(text="🔍 Найти проекты")],
        [KeyboardButton(text="🛠 Создать проект"), KeyboardButton(text="📈 Рекомендации")],
        [KeyboardButton(text="❓ Помощь")]
    ],

    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)

profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Изменить данные", callback_data="change_profile")],
        [InlineKeyboardButton(text="Мои проекты", callback_data="my_projects")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")],
    ]
)