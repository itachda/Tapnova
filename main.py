from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN
from play_interface import handle_play, tap_callback_handler
from leveling import handle_upgrade
from admin_panel import admin_dashboard, broadcast_handler

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("🚀 مرحبًا بك في TapNova!\nاستخدم زر 🚀 العب الآن للبدء.")

@dp.message_handler(text="🚀 العب الآن")
async def play(message: types.Message):
    await handle_play(message)

@dp.callback_query_handler(text="tap")
async def tap(callback_query: types.CallbackQuery):
    await tap_callback_handler(callback_query)

@dp.callback_query_handler(text="upgrade")
async def upgrade(callback_query: types.CallbackQuery):
    await handle_upgrade(callback_query)

@dp.message_handler(text="📊 لوحة التحكم")
async def admin(message: types.Message):
    await admin_dashboard(message)

@dp.message_handler(lambda m: m.chat.id in [123456789])
async def broadcast(message: types.Message):
    await broadcast_handler(message)

from database import init_db

if __name__ == "__main__":
    init_db()  # ← تأكد من وجود هذا السطر
    executor.start_polling(dp, skip_updates=True)
