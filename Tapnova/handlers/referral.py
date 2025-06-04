from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import main_menu
from database.db import count_user_referrals

router = Router()


@router.message(F.text == "🔗 إحالات")
async def show_referrals(message: Message):
    try:
        user_id = message.from_user.id

        referral_link = f"https://t.me/taonovas_bot?start={user_id}"

        referral_count = await count_user_referrals(user_id)
        total_nova = referral_count * 1000

        await message.answer(
            f"📎 رابط إحالتك:\n{referral_link}\n\n"
            f"👥 عدد الأشخاص الذين دعوتهُم: {referral_count}\n"
            f"💰 إجمالي النقاط المكتسبة: {total_nova} nova",
            reply_markup=main_menu
        )
    except Exception as e:
        await message.answer(f"❌ حدث خطأ أثناء عرض الإحالات: {e}")
