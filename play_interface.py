from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user_data, increment_clicks
import os
from PIL import Image

def get_planet_image(level: int) -> str:
    level = max(1, min(level, 30))
    return f"assets/planets/planet_{level}.png"

def get_background_image(level: int) -> str:
    level = max(1, min(level, 30))
    return f"assets/backgrounds/bg_{level}.png"

async def handle_play(message: types.Message):
    user = get_user_data(message.from_user.id)
    if not user:
        await message.answer("🚫 لم يتم العثور على بياناتك.")
        return

    level = user["level"]
    planet_path = get_planet_image(level)
    bg_path = get_background_image(level)

    if not os.path.exists(planet_path):
        await message.answer("🚫 صورة الكوكب غير موجودة.")
        return

    planet_img = Image.open(planet_path).convert("RGBA")
    if os.path.exists(bg_path):
        background = Image.open(bg_path).convert("RGBA").resize(planet_img.size)
        combined = Image.alpha_composite(background, planet_img)
    else:
        combined = planet_img

    temp_path = f"temp/combined_{message.from_user.id}.png"
    os.makedirs("temp", exist_ok=True)
    combined.save(temp_path)

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("👆 انقر الآن", callback_data="tap")
    )

    with open(temp_path, "rb") as photo:
        await message.answer_photo(photo, caption=f"🌍 المستوى {level}\\nانقر على الكوكب لتجميع النقاط!", reply_markup=keyboard)

async def tap_callback_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    increment_clicks(user_id, amount=1)
    await callback_query.answer("✅ تم احتساب نقرة!", show_alert=False)
