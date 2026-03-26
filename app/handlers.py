from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import F, Router
import app.keyboards as kb 

router = Router()

@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer("Добро пожаловать!", reply_markup=kb.main)

#Projects

@router.callback_query(F.data == "projects_menu")
async def to_projects_inline(callback: CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=kb.projects)
    await callback.answer()

#Profile

@router.callback_query(F.data == "user_profile")
async def to_profile_inline(callback: CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=kb.profile)
    await callback.answer()

#Help

@router.message(F.text == "❓ Помощь")
async def get_help(message: Message):
    await message.answer("")

@router.callback_query(F.data == "back_to_main")
async def back_to_main_inline(callback: CallbackQuery):
    await callback.message.edit_text("Вы вернулись в главное меню", reply_markup=kb.main)
    await callback.answer()

@router.callback_query(F.data == "sosiska")
async def get_help(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Сосо")