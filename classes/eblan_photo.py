import requests
from io import BytesIO
from PIL import Image, ImageOps

class EblanPhoto:
    def __init__(self, background_image_path, avatar_image):
        self.background_image = Image.open(background_image_path)
        self.avatar_image = self.download_image(avatar_image)

    def download_image(self, url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img

    def resize_image(self, size=(120, 120)):
        self.avatar_image = self.avatar_image.resize(size, Image.LANCZOS)

    def add_border(self, border_size=2, color='black'):
        self.avatar_image = ImageOps.expand(self.avatar_image, border=border_size, fill=color)

    def place_image(self, position=(0, 0)):
        self.background_image.paste(self.avatar_image, position) # 360x100

    def save_result(self, output_path='eblan_ready.png'):
        self.background_image.save(output_path)
        return output_path

