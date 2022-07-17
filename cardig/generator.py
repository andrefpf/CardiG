from pathlib import Path
from PIL import Image 
from PIL import ImageFont
from PIL import ImageDraw 


class Generator:
    def __init__(self, mockup):
        self.mockup = mockup
        self.mock_start = (0,0)
        self.mock_end = (0,0)
        self.mock_size = (0,0)

    @classmethod
    def from_configs(cls, config):
        mockup_config = config['mockup']
        cards_config = config['card']

        mockup = Image.open(mockup_config['path'])
        generator = cls(mockup)

        x0, y0 = mockup_config['title_pos']
        generator.set_title_location((x0,y0))

        x0,y0,x1,y1 = mockup_config['image_pos']
        generator.set_image_location((x0,y0), (x1,y1))

        x0,y0,x1,y1 = mockup_config['text_pos']
        generator.set_text_location((x0,y0), (x1,y1))

        for title, card in cards_config.items():
            img = Image.open(card['path'])
            generator.apply_in_image(img, title, card['text']).save(card['output'])

    def set_title_location(self, pos):
        self.title_pos = pos

    def set_image_location(self, start, end):
        self.mock_start = start
        self.mock_end = end
        self.mock_size = (self.mock_end[0] - self.mock_start[0],
                       self.mock_end[1] - self.mock_start[1])

    def set_text_location(self, start, end):
        self.text_start = start
        self.text_end = end
        self.text_size = (self.text_end[0] - self.text_start[0],
                       self.text_end[1] - self.text_start[1])

    def apply_in_image(self, image, title='', text=''):
        mask = None
        if image.mode == 'RGBA':
            mask = image.split()[3].resize(self.mock_size)
        image = image.resize(self.mock_size)

        mockuped = self.mockup.copy()
        mockuped.paste(image, self.mock_start, mask)
        
        title_font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 35)
        text_font = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 22)
        white = (255,255,255)
        black = (0,0,0)

        text = self._resize_text(text, text_font)

        draw = ImageDraw.Draw(mockuped)
        draw.text(self.title_pos, title, black, font=title_font, anchor="mm")
        draw.multiline_text(self.text_start, text, black, font=text_font)

        return mockuped

    def apply_in_images(self, images):
        applied = []
        for image in images:
            ap = self.apply_in_image(image)
            applied.append(ap)
        return applied

    def _split_in_lines(self, text, line_size):
        last = 0
        last_space = 0

        spaces = [' ', '\n']

        for i, char in enumerate(text):
            if char in spaces:
                last_space = i

            diff = (i - last)
            if diff == line_size:
                yield text[last:last_space]
                last = last_space + 1
        yield text[last:len(text)]

    def _resize_text(self, text_string, font):
        ascent, descent = font.getmetrics()
        text_width = font.getmask(text_string).getbbox()[2]
        max_text_width = self.text_end[0] - self.text_start[0]
        max_chars = len(text_string) * max_text_width // text_width
        return '\n'.join(i for i in self._split_in_lines(text_string, max_chars))