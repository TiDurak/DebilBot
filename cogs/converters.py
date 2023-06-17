import base64

import discord
from discord.ext import commands


class Convert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def encode_b64(self, ctx, *, message):
        """Кодирует твоё сообщение в формате BASE64"""

        text_bytes = message.encode('utf-8')  # Кодируем текст в байтовую последовательность
        base64_bytes = base64.b64encode(text_bytes)  # Кодируем байты в base64
        base64_text = base64_bytes.decode('utf-8')

        embed = discord.Embed(color=0xff8080, title='Base64 Encoder', description=base64_text)
        await ctx.send(embed=embed)

    @commands.command()
    async def decode_b64(self, ctx, *, message):
        """Декодирует BASE64 текст в нормальный, охуенный текст"""

        base64_bytes = message.encode('utf-8')  # Кодируем base64 текст в байтовую последовательность
        text_bytes = base64.b64decode(base64_bytes)  # Декодируем base64 байты обратно в исходные байты
        decoded_text = text_bytes.decode('utf-8')

        embed = discord.Embed(color=0xff8080, title='Base64 Decoder', description=decoded_text)
        await ctx.send(embed=embed)

    @commands.command()
    async def encode_binary(self, ctx, *, message):
        """Кодирует твоё сообщение в бинарный код"""

        binary_code = ' '.join(format(ord(char), '08b') for char in message)

        embed = discord.Embed(color=0xff8080, title='Binary Encoder', description=binary_code)
        await ctx.send(embed=embed)

    @commands.command()
    async def decode_binary(self, ctx, *, message):
        """Декодирует бинарный код в нормальный, охуенный текст"""

        text = ''.join(chr(int(binary, 2)) for binary in message.split())

        embed = discord.Embed(color=0xff8080, title='Binary Decoder', description=text)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Convert(bot))
