from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
import app.keyboards as kb 

router = Router()

@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer("Добро пожаловать!", reply_markup=kb.main)

@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("Это помощь тебе, друн!")

@router.callback_query(F.data == "sosiska")
async def get_help(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Сосо")