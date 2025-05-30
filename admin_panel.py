import sqlite3
from aiogram import types
from config import ADMIN_IDS

def get_stats():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE last_active = date('now')")
    active_today = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(clicks), SUM(nova) FROM users")
    clicks, nova = cursor.fetchone()
    conn.close()
    return total_users, active_today, clicks or 0, nova or 0

# ✅ الدالة المطلوبة هنا
async def admin_dashboard(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    total_users, active_today, total_clicks, total_nova = get_stats()
    text = (
        f"👑 لوحة التحكم:\n\n"
        f"👥 عدد المستخدمين: {total_users}\n"
        f"📅 النشطين اليوم: {active_today}\n"
        f"🖱️ إجمالي النقرات: {total_clicks}\n"
        f"💎 إجمالي NOVA: {total_nova}"
    )
    await message.answer(text)

async def broadcast_handler(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    text = message.text
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()
    for (user_id,) in users:
        try:
            await message.bot.send_message(user_id, text)
        except:
            continue
