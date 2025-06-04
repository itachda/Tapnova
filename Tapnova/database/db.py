import aiosqlite

DB_PATH = "tapnova.db"


async def connect_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            level INTEGER DEFAULT 1,
            nova INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            referred_by INTEGER,
            last_login_date TIMESTAMP,
            follow_telegram BOOLEAN DEFAULT 0,
            follow_twitter BOOLEAN DEFAULT 0,
            follow_instagram BOOLEAN DEFAULT 0,
            follow_youtube BOOLEAN DEFAULT 0,
            follow_facebook BOOLEAN DEFAULT 0
        )
        """)
        await db.commit()


async def add_user_if_not_exists(user_id: int, first_name: str, referrer_id: int = None):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        user = await cursor.fetchone()
        await cursor.close()
        if not user:
            await db.execute("""
                INSERT INTO users (id, first_name, referred_by)
                VALUES (?, ?, ?)
            """, (user_id, first_name, referrer_id))
            await db.commit()


async def get_user_by_id(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT id, first_name, level, nova, clicks, referred_by,
                   follow_telegram, follow_twitter, follow_instagram,
                   follow_youtube, follow_facebook
            FROM users WHERE id = ?
        """, (user_id,))
        user = await cursor.fetchone()
        await cursor.close()
        return user


async def update_user(user_id: int, **kwargs):
    if not kwargs:
        return
    keys = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values())
    values.append(user_id)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"""
            UPDATE users SET {keys} WHERE id = ?
        """, values)
        await db.commit()


async def get_required_clicks_for_level(level: int) -> int:
    return 3000 * (2 ** (level - 1))


async def get_top_players(limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT id, first_name, nova FROM users ORDER BY nova DESC LIMIT ?
        """, (limit,))
        players = await cursor.fetchall()
        await cursor.close()
        return players


async def count_user_referrals(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT COUNT(*) FROM users WHERE referred_by = ?
        """, (user_id,))
        row = await cursor.fetchone()
        await cursor.close()
        return row[0] if row else 0


# ✅ إصلاح الخطأ: دالة إكمال المهمة
async def complete_task(user_id: int, task_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"""
            UPDATE users SET {task_name} = 1 WHERE id = ?
        """, (user_id,))
        await db.commit()
async def get_task_status(user_id: int, task_name: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(f"""
            SELECT {task_name} FROM users WHERE id = ?
        """, (user_id,))
        row = await cursor.fetchone()
        await cursor.close()
        return row[0] == 1 if row else False
async def add_referral_bonus(user_id: int, referrer_id: int):
    bonus_amount = 1000  # عدد nova لكل إحالة
    async with aiosqlite.connect(DB_PATH) as db:
        # أعط المكافأة للمُحيل
        await db.execute("UPDATE users SET nova = nova + ? WHERE id = ?", (bonus_amount, referrer_id))
        await db.commit()
