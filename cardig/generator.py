from pathlib import Path
from PIL import Image 
from PIL import ImageFont
from PIL import ImageDraw 


class Generator:
    def __init__(self, mockup, start=(0,0), end=(100,100)):
        self.mockup = mockup
        self.set_image_location(start, end)

    @classmethod
    def from_configs(cls, config):
        mockup_config = config['mockup']
        cards_config = config['card']

        mockup = Image.open(mockup_config['path'])
        start = (mockup_config['start_x'], mockup_config['start_y'])
        end = (mockup_config['end_x'], mockup_config['end_y'])

        generator = cls(mockup, start, end)

        for title, card in cards_config.items():
            img = Image.open(card['path'])
            generator.apply_in_image(img, title, card['text']).save(card['output'])

    def set_image_location(self, start, end):
        self.m_start = start
        self.m_end = end
        self.m_size = (self.m_end[0] - self.m_start[0],
                       self.m_end[1] - self.m_start[1])

    def apply_in_image(self, image, title='', text=''):
        mask = None
        if image.mode == 'RGBA':
            mask = image.split()[3].resize(self.m_size)
        image = image.resize(self.m_size)

        mockuped = self.mockup.copy()
        mockuped.paste(image, self.m_start, mask)
        
        title_font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 50)
        text_font = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 20)
        white = (255,255,255)
        black = (0,0,0)

        draw = ImageDraw.Draw(mockuped)
        draw.text((368, 80), title, white, font=title_font, anchor="mm")
        draw.text((90, 900), text, black, font=text_font)



        return mockuped

    def apply_in_images(self, images):
        applied = []
        for image in images:
            ap = self.apply_in_image(image)
            applied.append(ap)
        return applied
