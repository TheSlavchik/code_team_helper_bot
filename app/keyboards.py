from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Мой профиль", callback_data="user_profile"),
            InlineKeyboardButton(text="🔍 Проекты", callback_data="projects_menu")
        ],
        [
            InlineKeyboardButton(text="❓ Помощь", callback_data="help_menu")
        ]
    ]
)


profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👤 Изменить данные профиля", callback_data="change_profile")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ]
)

projects = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Мои проекты", callback_data="test"), 
            InlineKeyboardButton(text="Создать проект", callback_data="test")
        ],
        [
            InlineKeyboardButton(text="Поиск по проектам", callback_data="test"),
            InlineKeyboardButton(text="Рекомендации", callback_data="test")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back_to_main")
        ]
    ]
)

test = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Изменить данные", callback_data="change_profile")],
        [InlineKeyboardButton(text="Мои проекты", callback_data="my_projects")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")],
    ]
)
create_project = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Введите название проекта',callback_data='create_project')],
    ]
)