from aiogram import Bot
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

# دالة إرسال إشعار لأي مستخدم
async def send_notification(user_id: int, text: str):
    try:
        await bot.send_message(user_id, text)
    except Exception as e:
        print(f"❌ فشل إرسال الإشعار إلى {user_id}: {e}")
