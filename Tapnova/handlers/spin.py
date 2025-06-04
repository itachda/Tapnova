from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import main_menu
from database.db import get_user_by_id, update_user
from utils.constants import get_required_clicks_for_level
import random

router = Router()

@router.message(F.text == "🎰 SPIN")
async def show_spin(message: Message):
    await message.answer("تم فتح واجهة SPIN 🎰")

    if not user:
        await message.answer("❌ لم يتم العثور على حسابك.", reply_markup=main_menu)
        return

    spins = user[5]   # عمود SPIN
    nova = user[3]
    clicks = user[4]
    level = user[2]

    if spins < 1:
        await message.answer("❌ لا تملك SPIN حالياً.\n💡 تحصل على 5 SPIN يوميًا تلقائيًا.", reply_markup=main_menu)
        return

    # 👇 احتمالات الجوائز (بسيطة وعادلة)
    rewards = [
        {"type": "nova", "value": 1000, "chance": 25},
        {"type": "nova", "value": 5000, "chance": 15},
        {"type": "spin", "value": 5, "chance": 10},
        {"type": "spin", "value": 10, "chance": 5},
        {"type": "spin", "value": 25, "chance": 2},
        {"type": "progress", "value": 10, "chance": 20},
        {"type": "progress", "value": 25, "chance": 15},
        {"type": "progress", "value": 40, "chance": 8},
    ]

    # 🎲 اختيار الجائزة عشوائيًا
    pool = []
    for reward in rewards:
        pool.extend([reward] * reward["chance"])
    reward = random.choice(pool)

    reward_text = ""
    new_values = {"spins": spins - 1}

    if reward["type"] == "nova":
        nova += reward["value"]
        new_values["nova"] = nova
        reward_text = f"💰 ربحت {reward['value']} nova!"
    elif reward["type"] == "spin":
        spins += reward["value"] - 1  # -1 لأننا خصمنا spin مسبقًا
        new_values["spins"] = spins
        reward_text = f"🔁 ربحت {reward['value']} SPIN!"
    elif reward["type"] == "progress":
        required_clicks = get_required_clicks_for_level(level)
        remaining = required_clicks - clicks
        gained = int(remaining * (reward["value"] / 100))
        clicks += gained
        new_values["clicks"] = clicks
        reward_text = f"🚀 تم كسر {reward['value']}٪ من مستواك الحالي!\n+{gained} نقرة"

    await update_user(user_id, **new_values)

    await message.answer(
        f"🎡 <b>نتيجة SPIN:</b>\n\n{reward_text}",
        reply_markup=main_menu
    )
