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
            InlineKeyboardButton(text="📋 Мои проекты", callback_data="my_projects"),
            InlineKeyboardButton(text="🚀 Создать проект", callback_data="create_project")
        ],
        [
            InlineKeyboardButton(text="🔍 Поиск по проектам", callback_data="search_projects"),
            InlineKeyboardButton(text="⭐ Рекомендации", callback_data="recommendations")
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

back_to_projects = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад к проектам", callback_data="projects_menu")]
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
project_name_step = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="projects_menu")]
    ]
)

# Шаг 2: Введите описание проекта
project_description_step = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="project_back_to_name")]
    ]
)


# === Project Detail & Edit keyboards ===

def get_project_detail_keyboard(project_id: int, is_owner: bool = False):
    """Клавиатура для просмотра деталей проекта"""
    buttons = []
    if is_owner:
        buttons.append([
            InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit_project_{project_id}"),
            InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_project_{project_id}")
        ])
    buttons.append([
        InlineKeyboardButton(text="🔙 Назад к списку", callback_data="my_projects")
    ])
    buttons.append([
        InlineKeyboardButton(text="🔙 В меню проектов", callback_data="projects_menu")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Клавиатура для шага выбора, что редактировать в проекте
def get_edit_project_choice_keyboard(project_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📌 Название", callback_data=f"edit_name_{project_id}")],
            [InlineKeyboardButton(text="📝 Описание", callback_data=f"edit_desc_{project_id}")],
            [InlineKeyboardButton(text="🛠 Технологии", callback_data=f"edit_reqs_{project_id}")],
            [InlineKeyboardButton(text="✅ Завершить редактирование", callback_data=f"finish_edit_{project_id}")],
        ]
    )


# Клавиатура для шага редактирования названия — назад к выбору поля
def edit_back_to_choice_keyboard(project_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад к выбору", callback_data=f"show_edit_menu_{project_id}")]
        ]
    )


# === Profile skills keyboard (used during project creation) ===
def get_profile_skills_keyboard(skills, rank):
    buttons = []
    if skills and skills != "Нет данных":
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
        
    if not buttons:
        buttons.append([InlineKeyboardButton(
            text="❌ Профиль не заполнен", 
            callback_data="empty_profile"
        )])
        
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === Popular techs for requirements ===
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
    row = []
    for text, callback in POPULAR_TECHS:
        row.append(InlineKeyboardButton(text=text, callback_data=callback))
        if len(row) == 2:
            inline_keyboard.append(row)
            row = []
    if row:
        inline_keyboard.append(row)
    
    inline_keyboard.append([
        InlineKeyboardButton(text="✅ Завершить создание проекта", callback_data="complete_project")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)