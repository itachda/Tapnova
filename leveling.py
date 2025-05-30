import sqlite3
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user_data
from play_interface import handle_play

# متطلبات كل مستوى
LEVEL_REQUIREMENTS = {
    1: 3000, 2: 6000, 3: 12000, 4: 24000, 5: 48000,
    6: 96000, 7: 192000, 8: 384000, 9: 768000, 10: 1536000,
    11: 3072000, 12: 6144000, 13: 12288000, 14: 24576000, 15: 49152000,
    16: 98304000, 17: 196608000, 18: 393216000, 19: 786432000, 20: 1572864000,
    21: 3145728000, 22: 6291456000, 23: 12582912000, 24: 25165824000,
    25: 50331648000, 26: 100663296000, 27: 201326592000, 28: 402653184000,
    29: 805306368000, 30: 1610612736000,
}

# ترقية مستوى المستخدم في قاعدة البيانات
def upgrade_user_level(user_id: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET level = level + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# التحقق إن كان المستخدم مؤهل للترقية
async def check_upgrade(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user = get_user_data(user_id)
    level = user['level']
    clicks = user['clicks']
    required = LEVEL_REQUIREMENTS.get(level, 999999999)

    if clicks >= required:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🚀 ترقية", callback_data="upgrade")
        )
        await callback_query.message.answer(
            f"🎉 وصلت إلى الحد المطلوب للترقية في المستوى {level}!",
            reply_markup=keyboard
        )

# تنفيذ الترقية
async def handle_upgrade(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    upgrade_user_level(user_id)
    await callback_query.message.answer("🚀 تم الترقية! استمتع بالكوكب الجديد 🎉")
    await handle_play(callback_query.message)
