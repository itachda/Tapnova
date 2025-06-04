from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text == "🎁 الهدايا / الإشعارات")
async def show_notifications(message: Message):
    await message.answer("📢 لا توجد إشعارات حالياً. تابعنا لكل جديد!", reply_markup=main_menu)

