import discord
from discord.ext import commands

import json
import requests

class Convert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def encode_b64(self, ctx, *, arg):
        response = requests.get(f'https://some-random-api.ml/base64?encode={arg}')
        json_data = json.loads(response.text)

        embed = discord.Embed(color = 0xff8080, title = 'Base64 Encoder', description = json_data['base64'])
        await ctx.send(embed = embed)

    @commands.command()
    async def decode_b64(self, ctx, *, arg):
        response = requests.get(f'https://some-random-api.ml/base64?decode={arg}')
        json_data = json.loads(response.text)

        embed = discord.Embed(color = 0xff8080, title = 'Base64 Decoder', description = json_data['text'])
        await ctx.send(embed = embed)


    @commands.command()
    async def encode_binary(self, ctx, *, arg):
        response = requests.get(f'https://some-random-api.ml/binary?encode={arg}')
        json_data = json.loads(response.text)

        embed = discord.Embed(color = 0xff8080, title = 'Binary Encoder', description = json_data['binary'])
        await ctx.send(embed = embed)

    @commands.command()
    async def decode_binary(self, ctx, *, arg):
        response = requests.get(f'https://some-random-api.ml/binary?decode={arg}')
        json_data = json.loads(response.text)

        embed = discord.Embed(color = 0xff8080, title = 'Binary Decoder', description = json_data['text'])
        await ctx.send(embed = embed)

def setup(bot):
        bot.add_cog(Convert(bot))