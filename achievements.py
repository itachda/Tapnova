from aiogram import types
from database import get_user_data

# قائمة الإنجازات مع شروط التحقق
ACHIEVEMENTS = [
    ("🔥 7 أيام نشاط متتالية", lambda u: u['clicks'] >= 1000),  # مثال مؤقت
    ("🚀 تجاوز المستوى 5", lambda u: u['level'] >= 5),
    ("🌌 تجاوز المستوى 10", lambda u: u['level'] >= 10),
    ("💎 الوصول إلى 100000 نقرة", lambda u: u['clicks'] >= 100000),
    ("👑 الوصول إلى 1000 NOVA", lambda u: u['nova'] >= 1000),
    ("👥 إحالة 5 أصدقاء", lambda u: u['referrals'] >= 5),
]

# دالة عرض الإنجازات
async def show_achievements(message: types.Message):
    user = get_user_data(message.from_user.id)
    achieved = []

    for name, condition in ACHIEVEMENTS:
        if condition(user):
            achieved.append(f"✅ {name}")
        else:
            achieved.append(f"❌ {name}")

    text = "🎖️ إنجازاتك:\n\n" + "\n".join(achieved)
    await message.answer(text)
