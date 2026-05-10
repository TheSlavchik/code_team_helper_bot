from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import app.keyboards as kb
from app.database import (get_profile, save_project, get_projects_by_user,
                          get_project_by_id, update_project, delete_project,
                          get_all_projects)

router = Router()

# --- Популярные технологии для быстрого выбора ---
POPULAR_SKILLS = {
    "python": "🐍 Python",
    "javascript": "📜 JavaScript",
    "react": "⚛️ React",
    "fastapi": "🚀 FastAPI",
    "sql": "🗄 SQL",
    "docker": "🐳 Docker",
    "figma": "🎨 Figma"
}

class ProjectCreation(StatesGroup):
    name = State()
    description = State()
    selected_requirements = State()


class ProjectEdit(StatesGroup):
    """Состояния для редактирования проекта"""
    waiting_for_field = State()
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_requirements = State()


@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(
        "Code Team Helper — ваш помощник в мире разработки. Бот помогает находить проекты под ваш стек технологий, "
        "собирать команду для собственных идей, управлять задачами и документацией",
        reply_markup=kb.main
    )

@router.callback_query(F.data == "projects_menu")
async def to_projects_inline(callback: CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=kb.projects)
    await callback.answer()

@router.callback_query(F.data == "user_profile")
async def to_profile_inline(callback: CallbackQuery, state: FSMContext):
    if state:
        await state.clear()
    await callback.message.edit_text("Выберите действие:", reply_markup=kb.profile)
    await callback.answer()

@router.callback_query(F.data == "help_menu")
async def back_to_main_inline(callback: CallbackQuery):
    await callback.message.edit_text("Это меню информации!", reply_markup=kb.back_to_main)
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def back_to_main_callback(callback: CallbackQuery):
    await callback.message.edit_text("Вы вернулись в главное меню", reply_markup=kb.main)
    await callback.answer()

# ====================== МОИ ПРОЕКТЫ ======================

@router.callback_query(F.data == "my_projects")
async def show_my_projects(callback: CallbackQuery):
    user_id = callback.from_user.id
    projects = get_projects_by_user(user_id)
    active_projects = [p for p in projects if p["status"] == "active"]

    if not active_projects:
        await callback.message.edit_text(
            "📋 У вас пока нет проектов.\n\nСоздайте первый проект!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🚀 Создать проект", callback_data="create_project")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="projects_menu")]
            ])
        )
        await callback.answer()
        return

    text = "📋 *Ваши проекты:*\n\n"
    buttons = []
    for p in active_projects:
        text += f"🔹 *{p['name']}*\n   🛠 {p['requirements'] or 'Нет технологий'}\n\n"
        buttons.append([InlineKeyboardButton(
            text=f"👁 {p['name']}",
            callback_data=f"view_project_{p['id']}"
        )])

    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="projects_menu")])

    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("view_project_"))
async def view_project(callback: CallbackQuery):
    project_id = int(callback.data.split("_")[2])
    project = get_project_by_id(project_id)

    if project is None:
        await callback.message.edit_text(
            "❌ Проект не найден.",
            reply_markup=kb.back_to_projects
        )
        await callback.answer()
        return

    user_id = callback.from_user.id
    is_owner = project["creator_id"] == user_id

    tech_list = project["requirements"] if project["requirements"] else "Нет выбранных технологий"

    text = (
        f"📌 *{project['name']}*\n\n"
        f"📝 *Описание:* {project['description'] or 'Нет описания'}\n"
        f"🛠 *Технологии:* {tech_list}\n"
        f"👤 *Создатель:* {project['creator_nick']}\n"
        f"📅 *Создан:* {project['created_at']}\n"
        f"🆔 ID: `{project['id']}`"
    )

    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=kb.get_project_detail_keyboard(project_id, is_owner)
    )
    await callback.answer()


# ====================== УДАЛЕНИЕ ПРОЕКТА ======================

@router.callback_query(F.data.startswith("delete_project_"))
async def delete_project_handler(callback: CallbackQuery):
    project_id = int(callback.data.split("_")[2])
    project = get_project_by_id(project_id)

    if project is None:
        await callback.message.edit_text("❌ Проект не найден.", reply_markup=kb.back_to_projects)
        await callback.answer()
        return

    if project["creator_id"] != callback.from_user.id:
        await callback.answer("❌ Вы не можете удалить этот проект", show_alert=True)
        return

    await callback.message.edit_text(
        f"🗑 Вы уверены, что хотите удалить проект *{project['name']}*?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_{project_id}")],
            [InlineKeyboardButton(text="❌ Нет, отмена", callback_data=f"view_project_{project_id}")]
        ])
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_delete_"))
async def confirm_delete_handler(callback: CallbackQuery):
    project_id = int(callback.data.split("_")[2])
    delete_project(project_id)

    await callback.message.edit_text(
        "✅ Проект удалён.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 Мои проекты", callback_data="my_projects")],
            [InlineKeyboardButton(text="🔙 В меню проектов", callback_data="projects_menu")]
        ])
    )
    await callback.answer()


# ====================== РЕДАКТИРОВАНИЕ ПРОЕКТА ======================

@router.callback_query(F.data.startswith("edit_project_"))
async def edit_project_handler(callback: CallbackQuery, state: FSMContext):
    project_id = int(callback.data.split("_")[2])
    project = get_project_by_id(project_id)

    if project is None:
        await callback.message.edit_text("❌ Проект не найден.", reply_markup=kb.back_to_projects)
        await callback.answer()
        return

    if project["creator_id"] != callback.from_user.id:
        await callback.answer("❌ Вы не можете редактировать этот проект", show_alert=True)
        return

    await state.update_data(edit_project_id=project_id)
    await state.set_state(ProjectEdit.waiting_for_field)

    await callback.message.edit_text(
        f"✏️ *Редактирование проекта:* {project['name']}\n\n"
        "Выберите, что хотите изменить:",
        parse_mode="Markdown",
        reply_markup=kb.get_edit_project_choice_keyboard(project_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("show_edit_menu_"))
async def show_edit_menu(callback: CallbackQuery, state: FSMContext):
    project_id = int(callback.data.split("_")[3])
    project = get_project_by_id(project_id)

    await state.set_state(ProjectEdit.waiting_for_field)

    await callback.message.edit_text(
        f"✏️ *Редактирование проекта:* {project['name']}\n\n"
        "Выберите, что хотите изменить:",
        parse_mode="Markdown",
        reply_markup=kb.get_edit_project_choice_keyboard(project_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("edit_name_"), ProjectEdit.waiting_for_field)
async def edit_name_start(callback: CallbackQuery, state: FSMContext):
    project_id = int(callback.data.split("_")[2])
    await state.set_state(ProjectEdit.waiting_for_name)
    await callback.message.edit_text(
        "✏️ Введите новое название проекта:",
        reply_markup=kb.edit_back_to_choice_keyboard(project_id)
    )
    await callback.answer()


@router.message(ProjectEdit.waiting_for_name)
async def edit_name_process(message: Message, state: FSMContext):
    data = await state.get_data()
    project_id = data.get("edit_project_id")
    new_name = message.text.strip()

    if not new_name:
        await message.answer("❌ Название не может быть пустым. Попробуйте снова:")
        return

    project = get_project_by_id(project_id)
    if project:
        update_project(project_id, new_name, project["description"],
                       project["requirements"].split(", ") if project["requirements"] else [])

    await state.set_state(ProjectEdit.waiting_for_field)
    await message.answer(
        f"✅ Название проекта изменено на: *{new_name}*",
        parse_mode="Markdown",
        reply_markup=kb.get_edit_project_choice_keyboard(project_id)
    )


@router.callback_query(F.data.startswith("edit_desc_"), ProjectEdit.waiting_for_field)
async def edit_desc_start(callback: CallbackQuery, state: FSMContext):
    project_id = int(callback.data.split("_")[2])
    await state.set_state(ProjectEdit.waiting_for_description)
    await callback.message.edit_text(
        "✏️ Введите новое описание проекта:",
        reply_markup=kb.edit_back_to_choice_keyboard(project_id)
    )
    await callback.answer()


@router.message(ProjectEdit.waiting_for_description)
async def edit_desc_process(message: Message, state: FSMContext):
    data = await state.get_data()
    project_id = data.get("edit_project_id")
    new_desc = message.text.strip()

    project = get_project_by_id(project_id)
    if project:
        update_project(project_id, project["name"], new_desc,
                       project["requirements"].split(", ") if project["requirements"] else [])

    await state.set_state(ProjectEdit.waiting_for_field)
    await message.answer(
        "✅ Описание проекта обновлено!",
        reply_markup=kb.get_edit_project_choice_keyboard(project_id)
    )


@router.callback_query(F.data.startswith("edit_reqs_"), ProjectEdit.waiting_for_field)
async def edit_reqs_start(callback: CallbackQuery, state: FSMContext):
    project_id = int(callback.data.split("_")[2])
    project = get_project_by_id(project_id)
    current = project["requirements"] if project and project["requirements"] else "не указаны"
    await state.set_state(ProjectEdit.waiting_for_requirements)
    await callback.message.edit_text(
        f"✏️ Введите новые технологии через запятую.\n\n"
        f"Текущие: *{current}*",
        parse_mode="Markdown",
        reply_markup=kb.edit_back_to_choice_keyboard(project_id)
    )
    await callback.answer()


@router.message(ProjectEdit.waiting_for_requirements)
async def edit_reqs_process(message: Message, state: FSMContext):
    data = await state.get_data()
    project_id = data.get("edit_project_id")
    text = message.text.strip()

    reqs = [r.strip() for r in text.split(",") if r.strip()]

    project = get_project_by_id(project_id)
    if project:
        update_project(project_id, project["name"], project["description"], reqs)

    await state.set_state(ProjectEdit.waiting_for_field)
    await message.answer(
        f"✅ Технологии обновлены: *{', '.join(reqs) or 'не указаны'}*",
        parse_mode="Markdown",
        reply_markup=kb.get_edit_project_choice_keyboard(project_id)
    )


@router.callback_query(F.data.startswith("finish_edit_"))
async def finish_edit_handler(callback: CallbackQuery, state: FSMContext):
    project_id = int(callback.data.split("_")[2])
    await state.clear()

    project = get_project_by_id(project_id)
    if project is None:
        await callback.message.edit_text("❌ Проект не найден.", reply_markup=kb.back_to_projects)
        await callback.answer()
        return

    tech_list = project["requirements"] if project["requirements"] else "Нет выбранных технологий"
    text = (
        f"✅ *Редактирование завершено!*\n\n"
        f"📌 *{project['name']}*\n"
        f"📝 {project['description'] or 'Нет описания'}\n"
        f"🛠 {tech_list}"
    )

    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=kb.get_project_detail_keyboard(project_id, is_owner=True)
    )
    await callback.answer()


# ====================== ПОИСК И РЕКОМЕНДАЦИИ ======================

@router.callback_query(F.data == "search_projects")
async def search_projects_handler(callback: CallbackQuery):
    all_projects = [p for p in get_all_projects() if p["status"] == "active"]

    if not all_projects:
        await callback.message.edit_text(
            "🔍 Активных проектов пока нет.",
            reply_markup=kb.back_to_projects
        )
        await callback.answer()
        return

    text = "🔍 *Все проекты:*\n\n"
    buttons = []
    for p in all_projects:
        text += f"🔹 *{p['name']}* — {p['creator_nick']}\n   🛠 {p['requirements'] or 'Нет технологий'}\n\n"
        buttons.append([InlineKeyboardButton(
            text=f"👁 {p['name']}",
            callback_data=f"view_project_{p['id']}"
        )])

    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="projects_menu")])

    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await callback.answer()


@router.callback_query(F.data == "recommendations")
async def recommendations_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    profile = get_profile(user_id)

    if profile is None or not profile["skills"]:
        await callback.message.edit_text(
            "⭐ Чтобы получить рекомендации, сначала заполните профиль.",
            reply_markup=kb.back_to_projects
        )
        await callback.answer()
        return

    user_skills = profile["skills"].lower()
    all_projects = [p for p in get_all_projects() if p["status"] == "active"]
    recommended = []

    for p in all_projects:
        reqs = p["requirements"].lower() if p["requirements"] else ""
        for skill in user_skills.split(", "):
            skill_clean = skill.strip()
            if skill_clean and skill_clean in reqs:
                recommended.append(p)
                break

    if not recommended:
        await callback.message.edit_text(
            "⭐ Не найдено проектов под ваш стек технологий.",
            reply_markup=kb.back_to_projects
        )
        await callback.answer()
        return

    text = "⭐ *Рекомендованные проекты:*\n\n"
    buttons = []
    for p in recommended:
        text += f"🔹 *{p['name']}* — {p['creator_nick']}\n   🛠 {p['requirements'] or 'Нет технологий'}\n\n"
        buttons.append([InlineKeyboardButton(
            text=f"👁 {p['name']}",
            callback_data=f"view_project_{p['id']}"
        )])

    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="projects_menu")])

    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await callback.answer()


# ====================== СОЗДАНИЕ ПРОЕКТА ======================

@router.callback_query(F.data == "create_project")
async def to_project_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProjectCreation.name)
    await callback.message.edit_text(
        "🚀 Создание нового проекта\n\nВведите название проекта:",
        reply_markup=kb.project_name_step
    )
    await callback.answer()

@router.message(ProjectCreation.name)
async def process_project_name(message: Message, state: FSMContext):
    project_name = message.text
    await state.update_data(name=project_name)
    await state.set_state(ProjectCreation.description)
    await message.answer(
        f"✅ Название: {project_name}\n\nВведите описание проекта:",
        reply_markup=kb.project_description_step
    )

@router.callback_query(F.data == "project_back_to_name")
async def back_to_project_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProjectCreation.name)
    await callback.message.edit_text(
        "Введите название проекта:",
        reply_markup=kb.project_name_step
    )
    await callback.answer()

@router.message(ProjectCreation.description)
async def process_project_description(message: Message, state: FSMContext):
    project_description = message.text
    await state.update_data(description=project_description)
    await state.set_state(ProjectCreation.selected_requirements)
    await state.update_data(selected_requirements=[])

    data = await state.get_data()
    skills = data.get('skills', 'Нет данных')
    rank = data.get('rank', 'Нет данных')

    await message.answer(
        f"👤 *Ваш профиль:*\n💻 Навыки: `{skills}`\n📊 Уровень: `{rank}`\n\n",
        reply_markup=kb.get_profile_skills_keyboard(skills, rank),
        parse_mode="Markdown"
    )

    await message.answer(
        "🛠 Этап 3/3. Выберите требования для проекта.\nНажмите на кнопку ниже или введите технологию текстом.",
        reply_markup=kb.get_tech_requirements_keyboard()
    )

@router.callback_query(F.data == "project_back_to_description")
async def back_to_project_description(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProjectCreation.description)
    data = await state.get_data()
    await callback.message.edit_text(
        f"✅ Название: {data.get('name', '')}\n\nВведите описание проекта:",
        reply_markup=kb.project_description_step
    )
    await callback.answer()

# === РАЗДЕЛЁННАЯ ЛОГИКА ТЕХНОЛОГИЙ ===

async def _update_requirements_message(message: Message, state: FSMContext):
    """Вспомогательная функция для обновления сообщения с текущими требованиями"""
    data = await state.get_data()
    reqs = data.get('selected_requirements', [])
    current_text = ", ".join(reqs) if reqs else "Пока ничего не выбрано"

    await message.answer(
        f"📌 Выбранные технологии: {current_text}\n\n"
        "Добавьте еще или нажмите 'Завершить' для сохранения проекта.",
        reply_markup=kb.get_tech_requirements_keyboard()
    )

@router.message(ProjectCreation.selected_requirements)
async def add_requirement_text(message: Message, state: FSMContext):
    """Добавление технологии текстом"""
    new_tech = message.text.strip()
    data = await state.get_data()
    reqs = data.get('selected_requirements', [])

    if new_tech not in reqs:
        reqs.append(new_tech)
        await state.update_data(selected_requirements=reqs)
        await _update_requirements_message(message, state)
    else:
        await message.answer(f"⚠️ Технология '{new_tech}' уже добавлена.", reply_markup=kb.get_tech_requirements_keyboard())

@router.callback_query(F.data.startswith("add_skill_"))
async def add_skill_from_profile(callback: CallbackQuery, state: FSMContext):
    """Добавление навыка из профиля"""
    skill = callback.data.split("_", 2)[2]
    data = await state.get_data()
    reqs = data.get('selected_requirements', [])

    if skill != "Нет данных" and skill not in reqs:
        reqs.append(skill)
        await state.update_data(selected_requirements=reqs)
        await callback.answer(f"✅ Добавлено: {skill}")
        await _update_requirements_message(callback.message, state)
    else:
        await callback.answer("Технология уже выбрана или недействительна", show_alert=True)

@router.callback_query(F.data.startswith("add_rank_"))
async def add_rank_from_profile(callback: CallbackQuery, state: FSMContext):
    """Добавление уровня как требования (если нужно)"""
    rank = callback.data.split("_", 2)[2]
    data = await state.get_data()
    reqs = data.get('selected_requirements', [])

    if rank != "Нет данных":
        if "rank:" not in [r.lower() for r in reqs]:
            reqs.append(f"Уровень: {rank}")
            await state.update_data(selected_requirements=reqs)
            await callback.answer(f"✅ Добавлено: Уровень {rank}")
            await _update_requirements_message(callback.message, state)
        else:
            await callback.answer("Уровень уже указан", show_alert=True)
    else:
        await callback.answer("Нет данных", show_alert=True)

@router.callback_query(F.data.startswith("pop_tech_"))
async def add_popular_tech(callback: CallbackQuery, state: FSMContext):
    """Добавление популярной технологии по ключу"""
    tech_key = callback.data.replace("pop_tech_", "")
    tech_name = POPULAR_SKILLS.get(tech_key, tech_key)

    data = await state.get_data()
    reqs = data.get('selected_requirements', [])

    if tech_key not in reqs:
        reqs.append(tech_key)
        await state.update_data(selected_requirements=reqs)
        await callback.answer(f"✅ Добавлено: {tech_key}")
        await _update_requirements_message(callback.message, state)
    else:
        await callback.answer("Уже в списке!", show_alert=True)

@router.callback_query(F.data == "complete_project")
async def project_complete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get('name', '')
    description = data.get('description', '')
    requirements = data.get('selected_requirements', [])

    requirements_text = ', '.join(requirements) if requirements else 'Нет выбранных технологий'

    user_id = callback.from_user.id
    tg_username = callback.from_user.username or ""

    profile = get_profile(user_id)
    if profile and profile["name"]:
        creator_nick = profile["name"]
    else:
        creator_nick = tg_username if tg_username else f"user_{user_id}"

    project_id = save_project(
        creator_id=user_id,
        creator_nick=creator_nick,
        name=name,
        description=description,
        requirements=requirements,
    )

    await callback.message.edit_text(
        f"✅ Проект успешно создан!\n\n"
        f"📌 Название: {name}\n"
        f"📝 Описание: {description}\n"
        f"🛠 Технологии: {requirements_text}\n"
        f"👤 Создатель: {creator_nick}\n"
        f"🆔 ID проекта: {project_id}",
        reply_markup=kb.main
    )
    await state.clear()