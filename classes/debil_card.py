from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


class DebilCard:
    def __init__(self, holder, balance, card_path="assets/debil_card/basic.png"):
        self.__font = "arialbd.ttf"
        self.__holder = holder
        self.__balance = balance
        self.__image = Image.open(card_path).convert("RGBA")

    def __load_font(self, font_path, size):
        try:
            return ImageFont.truetype(font, size)
        except IOError:
            return ImageFont.load_default()

    def add_text(self):
        draw = ImageDraw.Draw(self.__image)
        font = ImageFont.truetype(self.__font, 36)
        amount_font = ImageFont.truetype(self.__font, 32)
        x = 15
        y = self.__image.height - 100

        draw.text((x, y), self.__holder, font=font, fill="white")

        draw.text((x, y + 45), self.__balance, font=amount_font, fill="white")

    def get_buffer(self):
        buffer = BytesIO()
        self.__image.save(buffer, format="PNG")

        buffer.seek(0)
        return buffer