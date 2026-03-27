from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router
import app.keyboards as kb

profile_router = Router()

class Profile(StatesGroup):
    name = State()
    skills = State()
    rank = State()

@profile_router.callback_query(F.data == "change_profile")
async def to_projects_inline(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Profile.name)
    await callback.message.edit_text("Введите ваше имя:", reply_markup=kb.create_profile)
    await callback.answer()

@profile_router.message(Profile.name)
async def to_projects_inline(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Profile.skills)
    await message.answer("Выберите ваши навыки:", reply_markup=kb.skills)

@profile_router.callback_query(Profile.skills)
async def process_skills(callback: CallbackQuery, state: FSMContext):
    if callback.data == "user_skill_variant":
        await callback.message.edit_text("Напишите свой вариант:", reply_markup=kb.create_profile)
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
    await callback.message.edit_text("Выберите ваш уровень разработки:", reply_markup=kb.rank)
    await callback.answer()

@profile_router.message(Profile.skills)
async def process_custom_skill(message: Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await state.set_state(Profile.rank)
    await message.answer("Выберите ваш уровень разработки:", reply_markup=kb.rank)

@profile_router.callback_query(Profile.rank)
async def to_projects_inline(callback: CallbackQuery, state: FSMContext):
    button_text = "Неизвестно"
    for row in callback.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data:
                button_text = button.text
                break

    await state.update_data(rank=button_text)
    data = await state.get_data()
    await callback.message.edit_text(f"Ваши данные: {data["name"]}, {data["skills"]}, {data["rank"]}", reply_markup=kb.create_profile)
    await callback.answer()
    await state.clear()