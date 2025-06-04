from aiogram import Router, F
from aiogram.types import Message
from database.db import get_top_players
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text == "🥇 المتصدرون")
async def show_leaderboard(message: Message):
    top_players = await get_top_players()

    caption = "\U0001F4CA قائمة المتصدرين:\n\n"
    for idx, player in enumerate(top_players, start=1):
        caption += f"{idx}. {player[1]} - {player[2]} nova\n"

    await message.answer(caption, reply_markup=main_menu)
