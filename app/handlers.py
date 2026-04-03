from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
import app.keyboards as kb
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer("Code Team Helper — ваш помощник в мире разработки. Бот помогает находить проекты под ваш стек технологий, собирать команду для собственных идей, управлять задачами и документацией", reply_markup=kb.main)

#Projects

@router.callback_query(F.data == "projects_menu")
async def to_projects_inline(callback: CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=kb.projects)
    await callback.answer()

#Profile

@router.callback_query(F.data == "user_profile")
async def to_profile_inline(callback: CallbackQuery, state: FSMContext):
    if state:
        await state.clear()
    await callback.message.edit_text("Выберите действие:", reply_markup=kb.profile)
    await callback.answer()

#Help

@router.callback_query(F.data == "help_menu")
async def back_to_main_inline(callback: CallbackQuery):
    await callback.message.edit_text("Это меню информации!", reply_markup=kb.back_to_main)
    await callback.answer()

#Back_to_main

@router.callback_query(F.data == "back_to_main")
async def back_to_main_inline(callback: CallbackQuery):
    await callback.message.edit_text("Вы вернулись в главное меню", reply_markup=kb.main)
    await callback.answer()