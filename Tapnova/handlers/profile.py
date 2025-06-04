from aiogram import Router, F
from aiogram.types import Message
from database.db import get_user_by_id, get_required_clicks_for_level
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text == "👤 حسابي")
async def show_profile(message: Message):
    user_id = message.from_user.id
    user = await get_user_by_id(user_id)

    if not user:
        await message.answer("❌ لم يتم العثور على حسابك")
        return

    level = user[2]
    nova = user[3]
    clicks = user[4]
    required = await get_required_clicks_for_level(level)
    progress = (clicks / required) * 100

    await message.answer(
        f"👤 الملف الشخصي:\n"
        f"الاسم: {user[1]}\n"
        f"المستوى: {level}\n"
        f"النقرات: {clicks} / {required} ({progress:.1f}%)\n"
        f"عملة nova: {nova}",
        reply_markup=main_menu
    )