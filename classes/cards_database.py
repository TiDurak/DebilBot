import aiosqlite
from config import settings

class CardsDatabase:
    def __init__(self, database_path=settings.get("economics_db_path")):
        self.__database_path = database_path

    async def initialize(self):
        async with aiosqlite.connect(self.__database_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_items (
                    discord_id INTEGER PRIMARY KEY,
                    current_card TEXT NOT NULL DEFAULT 'basic'
                )
            """)

            await db.commit()

    async def get_current_card(self, discord_id: int) -> str:
        async with aiosqlite.connect(self.__database_path) as db:
            cursor = await db.execute(
                """
                SELECT current_card
                FROM user_items
                WHERE discord_id = ?
                """,
                (discord_id,)
            )

            row = await cursor.fetchone()

            if row is None:
                await db.execute(
                    """
                    INSERT INTO user_items (discord_id, current_card)
                    VALUES (?, 'basic')
                    """,
                    (discord_id,)
                )

                await db.commit()

                return "basic"

            return row[0]
