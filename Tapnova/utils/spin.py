import random

def get_spin_reward(level: int):
    # تحديد مكافأة nova حسب مستوى اللاعب
    if level <= 5:
        nova = random.randint(1000, 5000)
    elif level <= 15:
        nova = random.randint(3000, 10000)
    else:
        nova = random.randint(5000, 20000)

    # جدول الاحتمالات
    weighted = [
        ("nova", 50),              # 50% nova
        ("reduce_level_10", 15),   # 15% خصم 10%
        ("reduce_level_25", 10),   # 10% خصم 25%
        ("reduce_level_40", 5),    # 5% خصم 40%
        ("extra_spin", 20),        # 20% SPIN إضافية
    ]

    choice = random.choices(
        [item[0] for item in weighted],
        [item[1] for item in weighted]
    )[0]

    if choice == "nova":
        return ("nova", nova)
    elif choice == "reduce_level_10":
        return ("reduce_level", 0.10)
    elif choice == "reduce_level_25":
        return ("reduce_level", 0.25)
    elif choice == "reduce_level_40":
        return ("reduce_level", 0.40)
    elif choice == "extra_spin":
        return ("extra_spin", random.choice([5, 15, 25]))
