from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.main_menu import main_menu
from database.db import get_user_by_id, update_user, complete_task, get_task_status
from datetime import datetime, timedelta

router = Router()

# ✅ روابط المهام
SOCIAL_TASKS = {
    "telegram": ("📢 تابع قناة التلغرام", "https://t.me/tapnovaa"),
    "twitter": ("🐦 تابعنا على تويتر", "https://x.com/Tapnovas"),
    "instagram": ("📸 تابعنا على إنستغرام", "https://www.instagram.com/tapnovas?igsh=MTFweDV6d3N3OGI0NA=="),
    "youtube": ("▶️ اشترك في يوتيوب", "https://youtube.com/@tapnovas?si=hWtabBDw0RzFcHmj"),
    "facebook": ("📘 تابعنا على فيسبوك", "https://www.facebook.com/profile.php?id=61576925872593")
}

DAILY_REWARDS = {
    1: (100, 0),
    2: (200, 0),
    3: (500, 0),
    4: (800, 3),
    5: (1500, 0),
    6: (2500, 0),
    7: (0, 20)
}

@router.message(F.text == "📅 مهام يومية")
async def show_tasks(message: Message):
    await message.answer("هذه مهامك اليومية.")


    if not user:
        await message.answer("❌ لم يتم العثور على حسابك.")
        return

    day = user[8] or 1
    last_login = user[9]
    now = datetime.now()

    buttons = []

    # ⏰ تحقق من الانقطاع في الأيام
    if last_login:
        last_login_date = datetime.strptime(last_login, "%Y-%m-%d")
        if (now.date() - last_login_date.date()).days > 1:
            day = 1  # إعادة الدورة

    # 🏆 تسجيل الدخول اليومي
    buttons.append([
        InlineKeyboardButton(text=f"✅ سجل دخول يوم {day}", callback_data=f"daily_login:{day}")
    ])

    # 🌐 المهام الاجتماعية
    for key, (label, url) in SOCIAL_TASKS.items():
        task_done = await get_task_status(message.from_user.id, key)
        status = "✅" if task_done else "🔗"
        buttons.append([
            InlineKeyboardButton(text=f"{status} {label}", url=url),
            InlineKeyboardButton(text="تحقق", callback_data=f"check_task:{key}")
        ])

    await message.answer("📅 <b>مهام اليوم:</b>", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


@router.callback_query(F.data.startswith("daily_login:"))
async def claim_daily_login(callback: CallbackQuery):
    user = await get_user_by_id(callback.from_user.id)
    day = int(callback.data.split(":")[1])
    now = datetime.now()

    nova, spins = DAILY_REWARDS.get(day, (0, 0))
    new_nova = user[3] + nova
    new_spins = user[5] + spins

    next_day = 1 if day == 7 else day + 1

    await update_user(callback.from_user.id, nova=new_nova, spins=new_spins, daily_day=next_day, last_login=now.strftime("%Y-%m-%d"))

    await callback.message.answer(
        f"🎁 مكافأتك ليوم {day}:\n\n"
        f"💎 Nova: {nova}\n"
        f"🔁 SPIN: {spins}",
        reply_markup=main_menu
    )


@router.callback_query(F.data.startswith("check_task:"))
async def check_social_task(callback: CallbackQuery):
    task_key = callback.data.split(":")[1]
    user = await get_user_by_id(callback.from_user.id)

    already_done = await get_task_status(callback.from_user.id, task_key)
    if already_done:
        await callback.answer("✅ تم التحقق سابقًا.")
        return

    await complete_task(callback.from_user.id, task_key)
    new_nova = user[3] + 1000
    await update_user(callback.from_user.id, nova=new_nova)

    await callback.message.answer("✅ تم التحقق بنجاح!\n🎉 حصلت على 1000 nova", reply_markup=main_menu)
