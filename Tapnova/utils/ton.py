import requests

TON_API_KEY = "AFHSY54YS24EQHYAAAABPBEBHC5OLCHELI7QLHVCWQUUR4VFP7BAGZZI4KCOH76LOCJRNEI"
RECEIVER_ADDRESS = "UQCZUecR-YYZ3lOvqJo5ltPonK7bZ82b1K6ZCmEFhg4omPtp"
TON_API_URL = "https://tonapi.io/v2/blockchain/accounts"

# توليد رابط دفع باستخدام @wallet من تيليغرام
def generate_payment_link(user_id: int, usd_price: float):
    # سعر TON بالدولار — يمكن تعديله حسب السعر الحقيقي
    ton_price = 7.0
    amount_ton = round(usd_price / ton_price, 4)
    return f"https://t.me/wallet?startapp=transfer-{RECEIVER_ADDRESS}-{amount_ton}"

# التحقق من الدفع من TonAPI
async def check_payment(user_id: int) -> int:
    try:
        response = requests.get(
            f"{TON_API_URL}/{RECEIVER_ADDRESS}/transactions",
            headers={"Authorization": f"Bearer {TON_API_KEY}"}
        )
        txs = response.json().get("transactions", [])

        for tx in txs:
            comment = tx.get("payload", "")
            sender = tx.get("utime", 0)
            amount = int(tx.get("in_msg", {}).get("value", 0)) / 1e9  # Convert nanoTON

            if str(user_id) in comment and tx["in_msg"]["destination"] == RECEIVER_ADDRESS:
                # تحقق بناءً على المبلغ
                if 0.99 <= amount < 2: return 100
                elif 2 <= amount < 5: return 500
                elif 5 <= amount < 8: return 1000
                elif amount >= 8: return 2000

        return 0
    except Exception as e:
        print("خطأ في التحقق:", e)
        return 0
