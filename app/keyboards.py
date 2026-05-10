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

# На шаге ввода имени — назад к меню профиля
profile_name_step = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='user_profile')],
    ]
)

# На шаге выбора навыков — назад к шагу имени
skills = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Веб-разработка', callback_data='web'), InlineKeyboardButton(text='Мобильные приложения', callback_data='mobile')],
        [InlineKeyboardButton(text='Дизайн', callback_data='design'), InlineKeyboardButton(text='Маркетинг', callback_data='marketing')],
        [InlineKeyboardButton(text='Data Science', callback_data='data_science'), InlineKeyboardButton(text='Игры', callback_data='games')],
        [InlineKeyboardButton(text='Искусственный интеллект', callback_data='ai'), InlineKeyboardButton(text='1C', callback_data='1c')],
        [InlineKeyboardButton(text='Телеграм бот', callback_data='tgbot'), InlineKeyboardButton(text='Десктоп разработка', callback_data='desktop')],
        [InlineKeyboardButton(text='Напишите свой вариант', callback_data='user_skill_variant')],
        [InlineKeyboardButton(text='Назад', callback_data='profile_back_to_name')],
    ]
)

# На шаге ввода своего варианта навыка — назад к выбору навыков
custom_skill_step = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='profile_back_to_skills')],
    ]
)

# На шаге выбора уровня — назад к выбору навыков
rank = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Junior', callback_data='junior'), InlineKeyboardButton(text='Middle', callback_data='middle'), InlineKeyboardButton(text='Senior', callback_data='senior')],
        [InlineKeyboardButton(text='Назад', callback_data='profile_back_to_skills')],
    ]
)

# После завершения заполнения профиля
profile_finish = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='back_to_main')],
    ]
)

# Оставлено для обратной совместимости (если используется где-то ещё)
create_profile = profile_name_step
user_variant = custom_skill_step
