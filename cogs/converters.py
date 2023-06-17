import discord
from discord.ext import commands

import json
import requests


class Convert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def encode_b64(self, ctx, *, message):
        """Кодирует твоё сообщение в формате BASE64"""

        response = requests.get(f'https://some-random-api.com/base64?encode={message}')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xff8080, title='Base64 Encoder', description=json_data['base64'])
        await ctx.send(embed=embed)

    @commands.command()
    async def decode_b64(self, ctx, *, message):
        """Декодирует BASE64 текст в нормальный, охуенный текст"""

        response = requests.get(f'https://some-random-api.com/base64?decode={message}')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xff8080, title='Base64 Decoder', description=json_data['text'])
        await ctx.send(embed=embed)

    @commands.command()
    async def encode_binary(self, ctx, *, message):
        """Кодирует твоё сообщение в бинарный код"""

        response = requests.get(f'https://some-random-api.com/binary?encode={message}')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xff8080, title='Binary Encoder', description=json_data['binary'])
        await ctx.send(embed=embed)

    @commands.command()
    async def decode_binary(self, ctx, *, message):
        """Декодирует бинарный код в нормальный, охуенный текст"""

        response = requests.get(f'https://some-random-api.com/binary?decode={message}')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xff8080, title='Binary Decoder', description=json_data['text'])
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Convert(bot))
