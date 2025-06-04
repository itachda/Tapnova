from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.main_menu import main_menu
from database.db import add_user_if_not_exists, add_referral_bonus


router = Router()


@router.message(CommandStart(deep_link=True))
async def start_with_referral(message: Message, command: CommandStart):
    referrer_id = command.args
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    # تسجيل المستخدم إن لم يكن مسجلاً
    await create_user_if_not_exists(user_id, first_name)

    # إذا كان الرابط يحتوي على ID صحيح ولم يكن يحيل لنفسه
    if referrer_id and referrer_id.isdigit() and int(referrer_id) != user_id:
        await add_referral_bonus(user_id=user_id, referrer_id=int(referrer_id))

    await message.answer(
        f"👋 أهلاً <b>{first_name}</b> في <b>TapNova</b>!\n"
        f"🚀 اضغط على الأزرار لبدء اللعب واستكشاف المميزات!",
        reply_markup=main_menu
    )


@router.message(CommandStart())
async def start_without_referral(message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    await create_user_if_not_exists(user_id, first_name)

    await message.answer(
        f"👋 أهلاً <b>{first_name}</b> في <b>TapNova</b>!\n"
        f"🚀 اضغط على الأزرار لبدء اللعب واستكشاف المميزات!",
        reply_markup=main_menu
    )

