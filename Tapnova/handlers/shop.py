from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# رابط محفظة الدفع لكل باقة SPIN
TON_LINKS = {
    "100": "https://t.me/wallet/start?startapp=buy_100_spin",
    "500": "https://t.me/wallet/start?startapp=buy_500_spin",
    "1000": "https://t.me/wallet/start?startapp=buy_1000_spin",
    "2000": "https://t.me/wallet/start?startapp=buy_2000_spin"
}

@router.message(F.text == "🛒 المتجر")
async def show_shop(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌀 100 SPIN - 0.99 TON", url=TON_LINKS["100"])],
        [InlineKeyboardButton(text="🌀 500 SPIN - 3.99 TON", url=TON_LINKS["500"])],
        [InlineKeyboardButton(text="🌀 1000 SPIN - 6.99 TON", url=TON_LINKS["1000"])],
        [InlineKeyboardButton(text="🌀 2000 SPIN - 9.99 TON", url=TON_LINKS["2000"])]
    ])

    await message.answer(
        "🛍️ مرحبًا بك في المتجر!\n\nاختر الحزمة التي تريد شراءها وسيتم تحويلك لمحفظة Telegram للدفع.\nبعد إتمام الدفع، سيتم التحقق تلقائيًا من العملية وإضافة SPIN إلى حسابك ✅",
        reply_markup=keyboard
    )
