from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from scenarios.scenario_selection import show_start_message

router = Router()


@router.message(Command("model_info"))
async def show_model_info(message: Message, state: FSMContext):
    await message.answer(
        f"Здесь будет размещена информация об используемой модели предсказаний"
    )
    await show_start_message(message, state)
