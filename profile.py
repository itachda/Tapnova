from aiogram import types
from database import get_user_data

async def show_profile(message: types.Message):
    user = get_user_data(message.from_user.id)
    level = user['level']
    clicks = user['clicks']
    nova = user['nova']
    referrals = user['referrals']

    text = (
        f"👤 ملفك الشخصي:\n"
        f"🎮 المستوى: {level}\n"
        f"🖱️ عدد النقرات: {clicks}\n"
        f"💎 عملة NOVA: {nova}\n"
        f"👥 عدد الإحالات: {referrals}"
    )

    await message.answer(text)
