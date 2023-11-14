from PIL import Image, ImageDraw, ImageFont

class QuoteImageCreator:
    def __init__(self, background_image_path):
        self.background_image = Image.open(background_image_path)
        self.draw = ImageDraw.Draw(self.background_image)
        self.quote_font = self.load_font('timesi.ttf', size=16)
        self.author_font = self.load_font('timesbi.ttf', size=24)
        self.left_half_width = self.background_image.width // 2
        self.max_text_height = self.background_image.height * 0.8  # 80% вертикали

    def load_font(self, font_path, size):
        try:
            return ImageFont.truetype(font_path, size)
        except IOError:
            return ImageFont.load_default()

    def split_line(self, line, font, max_width):
        words = line.split()
        current_line = ""
        result_lines = []
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if self.draw.textbbox((0, 0), test_line, font=font)[2] <= max_width:
                current_line = test_line
            else:
                result_lines.append(current_line)
                current_line = word
        if current_line:
            result_lines.append(current_line)
        return result_lines

    def create_quote_image(self, content, author):
        content = f"\"{content}\""
        author = f"(c) {author}"
        if len(author) > 30:
            author = author[:30] + "..."

        text_lines = self.split_text(content)
        final_text_lines = self.split_long_lines(text_lines)

        self.fit_font_sizes(final_text_lines, author)

        self.draw_quote_text(final_text_lines)
        self.draw_author_text(author)

        self.background_image.save('quote.png')
        return 'quote.png'

    def split_text(self, content):
        max_line_length = 70
        words = content.split()
        current_line = ""
        text_lines = []
        for word in words:
            if len(current_line) + len(word) + 1 <= max_line_length:
                current_line = current_line + " " + word if current_line else word
            else:
                text_lines.append(current_line)
                current_line = word
        if current_line:
            text_lines.append(current_line)
        return text_lines

    def split_long_lines(self, text_lines):
        final_text_lines = []
        for line in text_lines:
            if self.draw.textbbox((0, 0), line, font=self.quote_font)[2] > self.left_half_width:
                final_text_lines.extend(self.split_line(line, self.quote_font, self.left_half_width))
            else:
                final_text_lines.append(line)
        return final_text_lines

    def get_text_height(self, font, lines):
        total_height = 0
        for line in lines:
            textbbox = self.draw.textbbox((0, 0), line, font=font)
            total_height += textbbox[3] - textbbox[1]
        return total_height

    def fit_font_size(self, font, text, max_height):
        while self.draw.textbbox((0, 0), text, font=font)[3] > max_height and font.size > 8:
            font.size -= 1

    def fit_font_sizes(self, text_lines, author):
        for line in text_lines:
            self.fit_font_size(self.quote_font, line, self.max_text_height)

        while self.get_text_height(self.quote_font, text_lines) > self.max_text_height and self.quote_font.size > 4:
            self.quote_font.size -= 2

        while self.draw.textbbox((0, 0), author, font=self.author_font)[3] > self.background_image.height and self.author_font.size > 8:
            self.author_font.size -= 1

    def draw_quote_text(self, text_lines):
        y = (self.background_image.height - self.get_text_height(self.quote_font, text_lines)) / 2
        for line in text_lines:
            textbbox = self.draw.textbbox((0, 0), line, font=self.quote_font)
            x = (self.left_half_width - textbbox[2]) / 2
            self.draw.text((x, y), line, fill='black', font=self.quote_font)
            y += textbbox[3] - textbbox[1]

    def draw_author_text(self, author):
        padding = 10
        author_bbox = self.draw.textbbox((0, 0), author, font=self.author_font)
        x = padding
        y = (self.background_image.height - author_bbox[3]) - padding
        self.draw.text((x, y), author, fill='black', font=self.author_font)