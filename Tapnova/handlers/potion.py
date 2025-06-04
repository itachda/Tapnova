from aiogram import Router, F
from aiogram.types import Message
from database.db import get_user_by_id, update_user
from keyboards.main_menu import main_menu
import random

router = Router()

@router.message(F.text == "🧪 قارورة سحرية")
async def use_potion(message: Message):
    user_id = message.from_user.id
    user = await get_user_by_id(user_id)

    if not user:
        await message.answer("❌ لم يتم العثور على حسابك")
        return

    nova = user[3]
    if nova < 10000:
        await message.answer("❌ تحتاج إلى 10000 nova لاستخدام القارورة السحرية.", reply_markup=main_menu)
        return

    await update_user(user_id, nova=nova - 10000)

    result = random.choices([
        ("✨ تم تخطي المستوى بالكامل!", 1.0),
        ("✨ تم تخطي نصف المستوى.", 0.5),
        ("✨ تم تخطي ربع المستوى.", 0.25)
    ], weights=[0.4, 0.3, 0.3])[0]

    await message.answer(result[0], reply_markup=main_menu)