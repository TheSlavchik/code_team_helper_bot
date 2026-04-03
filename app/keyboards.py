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

back_to_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ]
)

#Profile change

create_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад',callback_data='user_profile')],
    ]
)

skills = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Веб-разработка',callback_data='web'), InlineKeyboardButton(text='Мобильные приложения',callback_data='mobile')],
        [InlineKeyboardButton(text='Дизайн',callback_data='design'), InlineKeyboardButton(text='Маркетинг',callback_data='marketing')],
        [InlineKeyboardButton(text='Data Science',callback_data='data_science'), InlineKeyboardButton(text='Игры',callback_data='games')],
        [InlineKeyboardButton(text='Искусственный интеллект',callback_data='ai'), InlineKeyboardButton(text='1C',callback_data='1c')],
        [InlineKeyboardButton(text='Телеграм бот',callback_data='tgbot'), InlineKeyboardButton(text='Десктоп разработка',callback_data='desktop')],
        [InlineKeyboardButton(text='Напишите свой вариант',callback_data='user_skill_variant')],
    ]
)

rank = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Junior',callback_data='junior'), InlineKeyboardButton(text='Middle',callback_data='middle'), InlineKeyboardButton(text='Senior',callback_data='senior')]
    ]
)

user_variant = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад',callback_data='user_profile')],
    ]
)