import asyncio
from aiogram import Bot, Dispatcher
from handlers import (
    profile, spin, shop, tasks, achievements, leaderboard,
    notifications, potion, tutorial, events, start, referral
)
from database.db import connect_db

# 🛡️ توكن البوت (غيّره إلى توكنك الحقيقي)
bot = Bot(token="8062338258:AAFg6T0r343G5YvqyeG-Zmz7IAjhG1C8xJc", parse_mode="HTML")

# إعداد Dispatcher
dp = Dispatcher()

# ✅ تسجيل جميع الراوترات
dp.include_routers(
    start.router,
    spin.router,
    shop.router,
    profile.router,
    leaderboard.router,
    achievements.router,
    tasks.router,
    potion.router,
    tutorial.router,
    notifications.router,
    referral.router
)

# ✅ تشغيل البوت مع Polling
async def main():
    await connect_db()  # الاتصال بقاعدة البيانات
    await bot.delete_webhook(drop_pending_updates=True)  # إزالة التحديثات المتراكمة
    await dp.start_polling(bot)  # تشغيل البوت

if __name__ == "__main__":
    asyncio.run(main())
