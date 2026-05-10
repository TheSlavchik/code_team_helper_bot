from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router
import app.keyboards as kb
from app.database import save_profile, get_profile, profile_exists

profile_router = Router()


class Profile(StatesGroup):
    name = State()
    skills = State()
    custom_skill = State()
    rank = State()


# Просмотр профиля — читаем из БД
@profile_router.callback_query(F.data == "view_profile")
async def view_profile(callback: CallbackQuery):
    user_id = callback.from_user.id
    profile = get_profile(user_id)

    if profile is None:
        await callback.message.edit_text(
            "❌ У вас ещё нет профиля. Заполните его в разделе «Изменить данные профиля».",
            reply_markup=kb.back_to_main
        )
        await callback.answer()
        return

    text = (
        f"👤 *Ваш профиль*\n\n"
        f"🆔 ID: `{profile['user_id']}`\n"
        f"📝 Имя: {profile['name']}\n"
        f"💻 Навыки: {profile['skills']}\n"
        f"📊 Уровень: {profile['rank']}\n"
        f"📅 Создан: {profile['created_at']}"
    )
    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=kb.profile
    )
    await callback.answer()


# Старт заполнения профиля — шаг 1: ввод имени
@profile_router.callback_query(F.data == "change_profile")
async def start_profile(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Profile.name)
    await callback.message.edit_text(
        "Введите ваше имя:", reply_markup=kb.profile_name_step
    )
    await callback.answer()


# Шаг 1 -> 2: получили имя, спрашиваем навыки
@profile_router.message(Profile.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Profile.skills)
    await message.answer("Выберите ваши навыки:", reply_markup=kb.skills)


# Кнопка "Назад" с шага навыков -> возвращает на шаг ввода имени
@profile_router.callback_query(F.data == "profile_back_to_name")
async def back_to_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Profile.name)
    await callback.message.edit_text(
        "Введите ваше имя:", reply_markup=kb.profile_name_step
    )
    await callback.answer()


# Кнопка "Назад" с шагов rank/custom_skill -> возвращает на шаг выбора навыков
@profile_router.callback_query(F.data == "profile_back_to_skills")
async def back_to_skills(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Profile.skills)
    await callback.message.edit_text(
        "Выберите ваши навыки:", reply_markup=kb.skills
    )
    await callback.answer()


# Шаг 2: обработка выбора навыков (включая переход к "своему варианту")
@profile_router.callback_query(Profile.skills)
async def process_skills(callback: CallbackQuery, state: FSMContext):
    if callback.data == "user_skill_variant":
        await state.set_state(Profile.custom_skill)
        await callback.message.edit_text(
            "Напишите свой вариант:", reply_markup=kb.custom_skill_step
        )
        await callback.answer()
        return

    button_text = "Неизвестно"
    for row in callback.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data:
                button_text = button.text
                break

    await state.update_data(skills=button_text)
    await state.set_state(Profile.rank)
    await callback.message.edit_text(
        "Выберите ваш уровень разработки:", reply_markup=kb.rank
    )
    await callback.answer()


# Шаг 2b: пользователь ввёл свой вариант навыка текстом
@profile_router.message(Profile.custom_skill)
async def process_custom_skill(message: Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await state.set_state(Profile.rank)
    await message.answer(
        "Выберите ваш уровень разработки:", reply_markup=kb.rank
    )


# Шаг 3: выбор уровня — финальный экран с сохранением в БД
@profile_router.callback_query(Profile.rank)
async def process_rank(callback: CallbackQuery, state: FSMContext):
    button_text = "Неизвестно"
    for row in callback.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data:
                button_text = button.text
                break

    await state.update_data(rank=button_text)
    data = await state.get_data()

    user_id = callback.from_user.id
    tg_username = callback.from_user.username or ""

    # Сохраняем профиль в БД
    save_profile(
        user_id=user_id,
        tg_username=tg_username,
        name=data.get("name", ""),
        skills=data.get("skills", ""),
        rank=data.get("rank", ""),
    )

    await callback.message.edit_text(
        f"✅ Ваш профиль успешно заполнен и сохранён!\n\n"
        f"Имя: {data['name']}\n"
        f"Навыки: {data['skills']}\n"
        f"Уровень: {data['rank']}",
        reply_markup=kb.profile_finish,
    )
    await callback.answer()
    await state.clear()
