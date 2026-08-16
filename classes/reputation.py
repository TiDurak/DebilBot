import time
import aiosqlite
from config import settings

class Reputation:
    def __init__(self, db_path=settings.get("reputation_db_path")):
        self.__db_path = db_path
        self.__db = None

    async def initialize(self):
        self.__db = await aiosqlite.connect(self.__db_path)

        await self.__db.execute("""
            CREATE TABLE IF NOT EXISTS reputation (
                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                reputation INTEGER NOT NULL DEFAULT 0,
                last_given INTEGER,
                PRIMARY KEY (user_id, guild_id)
            )
        """)

        await self.__db.commit()

    async def give(self, user_id, guild_id, amount):
        now = int(time.time())
        cursor = await self.__db.execute("""
                SELECT last_given
                FROM reputation
                WHERE user_id = ? AND guild_id = ?
            """, (user_id, guild_id))

        result = await cursor.fetchone()

        if result is not None and result[0] is not None:
            remaining = 60 - (now - result[0])

            if remaining > 0:
                return {"success":False, "remaining":remaining}

        await self.__db.execute("""
                INSERT INTO reputation (
                    user_id,
                    guild_id,
                    reputation,
                    last_given
                )
                VALUES (?, ?, ?, ?)

                ON CONFLICT(user_id, guild_id)
                DO UPDATE SET
                    reputation = reputation + excluded.reputation,
                    last_given = excluded.last_given
            """, (user_id, guild_id, amount, now))

        await self.__db.commit()

        return {"success":True}

    async def get(self, user_id, guild_id):
        cursor = await self.__db.execute("""
            SELECT reputation
            FROM reputation
            WHERE user_id = ? AND guild_id = ?
        """, (user_id, guild_id))

        result = await cursor.fetchone()

        if result is None:
            return 0

        return result[0]

    async def close(self):
        if self.__db:
            await self.__db.close()