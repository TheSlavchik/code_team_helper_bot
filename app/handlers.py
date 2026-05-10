from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import app.keyboards as kb

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
    # Разделяем хранение: отдельно то, что уже выбрано (список)
    selected_requirements = State() 

@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer("Code Team Helper — ваш помощник в мире разработки. Бот помогает находить проекты под ваш стек технологий, собирать команду для собственных идей, управлять задачами и документацией", reply_markup=kb.main)

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

# === Project Creation Flow ===

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
    await state.update_data(selected_requirements=[]) # Инициализируем пустой список

    # Получаем эмулированные данные профиля (в реальном коде из БД/API)
    # Здесь оставляем, как у вас, для демонстрации. 
    # Лучше добавить await state.update_data(skills="...", rank="...") где-то раньше
    data = await state.get_data()
    skills = data.get('skills', 'Нет данных')
    rank = data.get('rank', 'Нет данных')

    # Отправляем ДВА сообщения подряд (можно сделать одно с reply_markup)
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
    skill = callback.data.split("_", 2)[2] # add_skill_Python -> Python
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

    # Пытаемся получить имя из профиля в БД
    from app.database import get_profile, save_project
    profile = get_profile(user_id)
    if profile and profile["name"]:
        creator_nick = profile["name"]
    else:
        creator_nick = tg_username if tg_username else f"user_{user_id}"

    # Сохраняем проект в БД
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

# Удалены старые хендлеры: process_project_requirements, project_requirements_step, select_requirements, add_requirement, handle_rank_callback