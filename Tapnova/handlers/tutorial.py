from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text == "📘 شرح")
async def show_tutorial(message: Message):
    photo = FSInputFile("media/tutorial/how_to_play.png")  # ← تأكد من وجود الصورة بهذا المسار

    caption = (
        "🛰 <b>مرحباً بك في TapNova!</b>\n\n"
        "🚀 لعبة نقر فضائية! قم بالنقر لزيادة نقاطك، اجمع نوفا، ارتقِ في المستويات، وافتح كواكب جديدة.\n\n"
        "🎡 استخدم SPIN للحصول على مكافآت يومية.\n"
        "🧪 استخدم القوارير السحرية للتقدم بسرعة في المستويات.\n"
        "📅 أتمم المهام اليومية لكسب المزيد من النوفا.\n"
        "👥 شارك رابط الإحالة لكسب 1000 nova عن كل صديق جديد!"
    )

    await message.answer_photo(photo, caption=caption, reply_markup=main_menu)
