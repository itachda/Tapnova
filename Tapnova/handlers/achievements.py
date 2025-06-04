from aiogram import Router, F
from aiogram.types import Message
from database.db import get_user_by_id
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text == "🏆 الإنجازات")
async def achievements_handler(message: Message):
    user_id = message.from_user.id
    user = await get_user_by_id(user_id)
    if not user:
        await message.answer("❌ لم يتم العثور على حسابك")
        return

    clicks = user[4]
    level = user[2]
    days_active = 0  # افتراضي الآن

    achievements = []
    if days_active >= 7:
        achievements.append("✅ 7 أيام نشاط متتالية")
    if days_active >= 15:
        achievements.append("✅ 15 يوم نشاط متتالي")
    if days_active >= 30:
        achievements.append("✅ 30 يوم نشاط")
    if days_active >= 90:
        achievements.append("✅ 90 يوم نشاط")
    if level > 5:
        achievements.append("✅ تجاوز المستوى 5")
    if level > 10:
        achievements.append("✅ تجاوز المستوى 10")
    if level > 20:
        achievements.append("✅ تجاوز المستوى 20")
    if level > 30:
        achievements.append("✅ تجاوز المستوى 30")
    if clicks >= 5000:
        achievements.append("✅ 5000 نقرة")
    if clicks >= 100000:
        achievements.append("✅ 100000 نقرة")

    if not achievements:
        achievements.append("لا توجد إنجازات بعد. واصل اللعب!")

    await message.answer("🏆 إنجازاتك:\n\n" + "\n".join(achievements), reply_markup=main_menu)
