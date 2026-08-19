import time
import aiosqlite
from config import settings

class Economics:
    DAILY_REWARD = 1000
    DAILY_COOLDOWN = 60 * 60 * 24

    def __init__(self, db_path=settings.get("economics_db_path")):
        self.__db_path = db_path
        self.__db = None

    async def initialize(self):
        self.__db = await aiosqlite.connect(self.__db_path)

        await self.__db.execute("""
            CREATE TABLE IF NOT EXISTS economics (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER NOT NULL DEFAULT 0,
                last_daily INTEGER
            )
        """)

        await self.__db.commit()

    async def get_balance(self, user_id):
        cursor = await self.__db.execute("""
            SELECT balance
            FROM economics
            WHERE user_id = ?
        """, (user_id,))

        result = await cursor.fetchone()

        if result is None:
            return 0

        return result[0]

    async def edit_money(self, user_id, amount):
        if amount == 0:
            return True
        if amount < 0:
            cursor = await self.__db.execute("""
                    SELECT balance
                    FROM economics
                    WHERE user_id = ?
                """, (user_id,))

            result = await cursor.fetchone()
            if result is None or result[0] < abs(amount):
                return False
            
        cursor = await self.__db.execute("""
            INSERT INTO economics (user_id, balance)
            VALUES (?, ?)

            ON CONFLICT(user_id)
            DO UPDATE SET
                balance = balance + excluded.balance
            WHERE balance + excluded.balance >= 0
        """, (user_id, amount))
        await self.__db.commit()
        return cursor.rowcount > 0

    async def get_daily(self, user_id):
        now = int(time.time())
        cursor = await self.__db.execute("""
            SELECT last_daily
            FROM economics
            WHERE user_id = ?
        """, (user_id,))
        result = await cursor.fetchone()

        if result and result[0] is not None:
            remaining = self.DAILY_COOLDOWN - (now - result[0])
            if remaining > 0:
                hours, remainder = divmod(remaining, 3600)
                minutes, seconds = divmod(remainder, 60)
                return False, f"{hours:02}:{minutes:02}:{seconds:02}"

        await self.edit_money(user_id, self.DAILY_REWARD)

        await self.__db.execute("""
            INSERT INTO economics (user_id, last_daily)
            VALUES (?, ?)

            ON CONFLICT(user_id)
            DO UPDATE SET last_daily = excluded.last_daily
        """, (user_id, now))

        await self.__db.commit()
        return True, None

    async def close(self):
        if self.__db is not None:
            await self.__db.close()