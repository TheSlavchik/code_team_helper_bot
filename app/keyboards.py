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
        [InlineKeyboardButton(text="👀 Просмотреть профиль", callback_data="view_profile")],
        [InlineKeyboardButton(text="✏️ Изменить данные профиля", callback_data="change_profile")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ]
)

projects = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Мои проекты", callback_data="test"), 
            InlineKeyboardButton(text="Создать проект", callback_data="create_project")
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

# === Project Creation keyboards ===

# Шаг 1: Введите название проекта
# Кнопка "Назад" возвращает на главный экран
project_name_step = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='← Назад к меню', callback_data='back_to_main')],
    ]
)

# Шаг 2: Введите описание проекта
# Кнопка "Назад" возвращает к шагу 1 (ввода названия)
project_description_step = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='← Назад к названию', callback_data='project_back_to_name')],
    ]
)

# Шаг 3: Выберите технологии из профиля
# Кнопка "Назад" возвращает к шагу 2 (ввода описания)
project_requirements_step = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='← Назад к описанию', callback_data='project_back_to_description')],
    ]
)

# Кнопка "Завершено" — вернуться на главный экран
project_complete = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅ Завершено', callback_data='project_complete')],
    ]
)


# --- Остальные ваши клавиатуры (main, projects, profile, back_to_main и т.д.) ---

project_name_step = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Назад", callback_data="projects_menu")]
])

project_description_step = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Назад", callback_data="project_back_to_name")]
])

# Клавиатура для меню профиля (навыки + уровень)
def get_profile_skills_keyboard(skills, rank):
    buttons = []
    if skills and skills != "Нет данных":
        # Предполагаем, что навыки могут быть списком или строкой
        skill_list = skills if isinstance(skills, list) else skills.split(", ")
        for skill in skill_list:
            skill = skill.strip()
            if skill:
                buttons.append([InlineKeyboardButton(
                    text=f"💻 Мой навык: {skill}", 
                    callback_data=f"add_skill_{skill}"
                )])
    
    if rank and rank != "Нет данных":
        buttons.append([InlineKeyboardButton(
            text=f"📊 Мой уровень: {rank}", 
            callback_data=f"add_rank_{rank}"
        )])
        
    # Если вообще нет данных
    if not buttons:
        buttons.append([InlineKeyboardButton(
            text="❌ Профиль не заполнен", 
            callback_data="empty_profile"
        )])
        
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура для быстрого выбора технологий (популярные)
POPULAR_TECHS = [
    ("🐍 Python", "pop_tech_python"),
    ("📜 JavaScript", "pop_tech_javascript"),
    ("⚛️ React", "pop_tech_react"),
    ("🚀 FastAPI", "pop_tech_fastapi"),
    ("🗄 SQL", "pop_tech_sql"),
    ("🐳 Docker", "pop_tech_docker"),
    ("🎨 Figma", "pop_tech_figma"),
]

def get_tech_requirements_keyboard():
    inline_keyboard = []
    
    # Разбиваем кнопки на ряды по 2
    row = []
    for text, callback in POPULAR_TECHS:
        row.append(InlineKeyboardButton(text=text, callback_data=callback))
        if len(row) == 2:
            inline_keyboard.append(row)
            row = []
    if row:
        inline_keyboard.append(row)
    
    # Кнопка завершения
    inline_keyboard.append([
        InlineKeyboardButton(text="✅ Завершить создание проекта", callback_data="complete_project")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)