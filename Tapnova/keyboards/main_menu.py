from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 نقر"), KeyboardButton(text="🎰 SPIN")],
        [KeyboardButton(text="🧪 قارورة سحرية"), KeyboardButton(text="🛒 المتجر")],
        [KeyboardButton(text="📅 مهام يومية"), KeyboardButton(text="📘 شرح")],
        [KeyboardButton(text="🏆 الإنجازات"), KeyboardButton(text="📊 الترتيب")],
        [KeyboardButton(text="👤 حسابي"), KeyboardButton(text="🔗 الإحالة")]
    ],
    resize_keyboard=True,
    input_field_placeholder="اختر أحد الأوامر 👇"
)
