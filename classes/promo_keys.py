from config import settings

import hashlib
import aiosqlite

class PromoKeys:
    def __init__(self, db_path=settings.get("promokeys_db_path")):
        self.__db_path = db_path
        self.__db = None

    async def initialize(self):
        self.__db = await aiosqlite.connect(self.__db_path)

    async def get_reward(self, key: str) -> int:
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        cursor = await self.__db.execute("""
            UPDATE redeem_keys
            SET is_used = TRUE
            WHERE key_hash = ?
              AND is_used = FALSE
            RETURNING reward
        """, (key_hash,))

        row = await cursor.fetchone()
        await self.__db.commit()

        if row is None:
            return 0

        return row[0]

    async def close(self):
        if self.__db is not None:
            await self.__db.close()