import time
import os
from PIL import Image, ImageDraw, ImageFont
from lib import epd2in7_V2
from radio import Radio

class RadioDisplay:
    font_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    font16 = ImageFont.truetype(os.path.join(font_dir, 'Audiowide-Regular.ttf'), 16)
    # font24 = ImageFont.truetype(os.path.join(font_dir, 'Audiowide-Regular.ttf'), 24)
    font48 = ImageFont.truetype(os.path.join(font_dir, 'Audiowide-Regular.ttf'), 48)
    font64 = ImageFont.truetype(os.path.join(font_dir, 'Audiowide-Regular.ttf'), 64)
    font96 = ImageFont.truetype(os.path.join(font_dir, 'Audiowide-Regular.ttf'), 96)
    # font = ImageFont.truetype(os.path.join(font_dir, 'Orbitron-VariableFont_wght.ttf'), 36)
    # font = ImageFont.truetype(os.path.join(font_dir, 'ShareTechMono-Regular.ttf'), 36)
    # font = ImageFont.load_default()

    BLACK = 0
    DARK_GRAY = 128
    LIGHT_GRAY = 192
    WHITE = 255

    def __init__(self, radio: Radio, epd: epd2in7_V2.EPD):
        self.radio = radio
        self.epd = epd
        # self.radio.add_observer(self.update_display_bw)
        self.radio.add_observer(self.update_display)
        # print the panel height and width -- 264 x 176
        # print(f"Panel Height: {self.epd.height}, Panel Width: {self.epd.width}")

    # portrait mode
    def print_text(self, text: str) -> None:
        image = Image.new('L', (self.epd.width, self.epd.height), self.WHITE)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, 10), text, font=font, fill=0)
        self.epd.display_4Gray(self.epd.getbuffer_4Gray(image))

    # landscape mode
    def update_display(self) -> None:

        self.epd.init_Fast()  # Wake up the display
        
        himage = Image.new('1', (self.epd.height, self.epd.width), self.WHITE) #255 : clear the frame
        draw = ImageDraw.Draw(himage)

        # top little status bar
        text = f"{self.radio.current_band.value} {self.radio.mode.value}"
        draw.text((5, 10), text, font=self.font16, fill=self.BLACK)

        text = f"{self.radio.wpm} WPM"
        draw.text((115, 10), text, font=self.font16, fill=self.BLACK)

        text = f"{self.radio.battery_voltage}V"
        draw.text((self.epd.height - 40, 10), text, font=self.font16, fill=self.BLACK)

        text = f"{self.radio.frequency:.4f}"
        draw.text((10, 30), text, font=self.font48, fill=self.BLACK)

        self.epd.display_Fast(self.epd.getbuffer(himage))

        self.epd.sleep()        # Enter sleep mode

    # TODO a partial refresh of the screen for just the Frequency
    
    def Splash(self) -> None:
        himage = Image.new('L', (self.epd.height, self.epd.width), self.WHITE) #255 : clear the frame
        draw = ImageDraw.Draw(himage)
        draw.text((10, -20), "QRP", font=self.font96, fill=self.BLACK)
        draw.text((10, 80), "Power!", font=self.font64, fill=self.LIGHT_GRAY)
        self.epd.display_4Gray(self.epd.getbuffer_4Gray(himage))

        time.sleep(2)
        self.epd.Clear()

    def QRT(self) -> None:
        self.epd.init_Fast()  # Wake up the display
        himage = Image.new('1', (self.epd.height, self.epd.width), self.WHITE) #255 : clear the frame
        draw = ImageDraw.Draw(himage) 
        draw.text((5,28), "QRT!", font=self.font96, fill=self.BLACK)
        self.epd.display_Fast(self.epd.getbuffer(himage))

        time.sleep(0.5)

    def clear(self) -> None:
        self.epd.Clear()

    def clearSleep(self) -> None:
        self.epd.Clear()        # Clear display first
        time.sleep(0.2)         # Brief pause to ensure clear completes
        self.epd.sleep()        # Enter sleep mode

# 255 = white
# 192 = light gray
# 128 = dark gray
# 0 = black