import discord
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def deleted(self, ctx, cmd_name: str):
        await ctx.send(f"Эта команда больше не работает. Вместо неё используйте `{cmd_name}`")

    @commands.command()
    async def play(self, ctx):
        """Воспроизводит песню с YouTube, или добавляет её в список, если сейчас играет другая песня.
        Эта команда больше не работает. Вместо неё используйте /play"""
        await self.deleted(ctx, "/play")

    @commands.command()
    async def skip(self, ctx):
        """Пропускает текущую песню.
        Эта команда больше не работает. Вместо неё используйте /skip"""
        await self.deleted(ctx, "/skip")

    @commands.command(name="queue")
    async def queue_embed(self, ctx):
        """Показывает список следующих песен.
        Эта команда больше не работает. Вместо неё используйте /queue"""
        await self.deleted(ctx, "/queue")

    @commands.command()
    async def leave(self, ctx):
        """Кикает бота из голосового чата.
        Эта команда больше не работает. Вместо неё используйте /leave"""
        await self.deleted(ctx, "/leave")

    @commands.command()
    async def stop(self, ctx):
        """Останавливает текущую песню, и очищает список проигрывания.
        Эта команда больше не работает. Вместо неё используйте /stop"""
        await self.deleted(ctx, "/stop")

    @commands.command()
    async def pause(self, ctx):
        """Ставит песню на паузу.
        Эта команда больше не работает. Вместо неё используйте"""
        await self.deleted(ctx, "/switch_pause")

    @commands.command()
    async def resume(self, ctx):
        """То же самое, что и пауза, только наоборот (ты лох, и докажи что нет).
        Эта команда больше не работает. Вместо неё используйте /switch_pause"""
        await self.deleted(ctx, "/switch_pause")


async def setup(bot):
    await bot.add_cog(Music(bot))
