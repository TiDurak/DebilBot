import base64
import hashlib

import discord
from discord import app_commands
from discord.ext import commands


class SConverters(commands.Cog):
    """Converters"""

    def __init__(self, bot):
        self.bot = bot

    class Encoder:
        @staticmethod
        def encode_b64(text: str) -> str:
            text_bytes = text.encode('utf-8')
            base64_bytes = base64.b64encode(text_bytes)
            base64_text = base64_bytes.decode('utf-8')
            return base64_text

        @staticmethod
        def decode_b64(b64_text: str) -> str:
            base64_bytes = b64_text.encode('utf-8')
            text_bytes = base64.b64decode(base64_bytes)
            decoded_text = text_bytes.decode('utf-8')
            return decoded_text

        @staticmethod
        def encode_binary(text: str):
            binary_code = ' '.join(format(ord(char), '08b') for char in text)
            return binary_code

        @staticmethod
        def decode_binary(binary_code: str):
            text = ''.join(chr(int(binary, 2)) for binary in binary_code.split())
            return text

    @app_commands.command(name="code",
                          description="кодирует/ декодирует твой недотекст/недокод")
    @app_commands.describe(method="Метод кодирования",
                           code_or_decode="Кодировать или декодировать",
                           message="Твой недотекст или код нахуй")
    @app_commands.choices(method=[
        app_commands.Choice(name="Base64", value="b64"),
        app_commands.Choice(name="Бинарный Код", value="binary"),
    ], code_or_decode=[
        app_commands.Choice(name="Кодирование", value="encode"),
        app_commands.Choice(name="Декодирование", value="decode"),
    ])
    async def code(self, interaction: discord.Interaction,
                   method: app_commands.Choice[str],
                   code_or_decode: app_commands.Choice[str],
                   message: str):
        output = None
        coder = self.Encoder()
        if method.value == "b64":
            if code_or_decode.value == "encode":
                output = coder.encode_b64(message)
            elif code_or_decode.value == "decode":
                output = coder.decode_b64(message)
        elif method.value == "binary":
            if code_or_decode.value == "encode":
                output = coder.encode_binary(message)
            elif code_or_decode.value == "decode":
                output = coder.decode_binary(message)

        embed = discord.Embed(color=0xffcd4c, title="Кодировка нахер")
        embed.add_field(name="Исходный Текст", value=message, inline=False)
        embed.add_field(name=f"Метод Кодирования", value=f"{method.name}, {code_or_decode.name}", inline=False)
        embed.add_field(name=f"Выход", value=output, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hash",
                          description="хеширует твой недотекст")
    @app_commands.describe(method="Метод хеширования",
                           text="Твой недотекст нахуй")
    @app_commands.choices(method=[
        app_commands.Choice(name="SHA1", value="sha1"),
        app_commands.Choice(name="SHA256", value="sha256"),
        app_commands.Choice(name="SHA512", value="sha512"),
        app_commands.Choice(name="MD5", value="md5"),

    ])
    async def hash(self, interaction: discord.Interaction,
                   method: app_commands.Choice[str],
                   text: str):
        hash_object = None
        if method.value == "sha1":
            hash_object = hashlib.sha1(text.encode())
        if method.value == "sha256":
            hash_object = hashlib.sha256(text.encode())
        if method.value == "sha512":
            hash_object = hashlib.sha512(text.encode())
        elif method.value == "md5":
            hash_object = hashlib.md5(text.encode())
        hex_dig = hash_object.hexdigest()

        embed = discord.Embed(color=0xffcd4c, title="Хеширатор блэт")
        embed.add_field(name="Исходный Текст", value=text, inline=False)
        embed.add_field(name=f"Метод Хеширования: {method.name}", value=hex_dig, inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(SConverters(bot))