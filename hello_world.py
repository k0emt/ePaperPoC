import sys
sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys

from lib import epd2in7_V2

from PIL import Image, ImageDraw, ImageFont
import time
from gpiozero import Button

def printToDisplay(text):
    # Create a blank image for drawing
    image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.load_default()

    # Draw the text on the image
    draw.text((10, 10), text, font=font, fill=0)  # 0: black

    # Display the image on the e-paper display
    epd.display(epd.getbuffer(image))
    # epd.sleep()        # put the display to sleep

# main program

if __name__ == '__main__':
    print("Program start...") # prints to console, not the display, for debugging
    epd = epd2in7_V2.EPD() # get the display
    epd.init()           # initialize the display
    print("writing to e-Paper display...") # prints to console, not the display, for debugging
    printToDisplay("Hello, world! ZZZZzz") # prints to the display

    time.sleep(3)

    print("clearing display...") # prints to console, not the display, for debugging

    epd.Clear()        # corrected method call
    epd.sleep()        # put the display to sleep

# from gpiozero import Button
# Key 1, pin 5
# Key 2, pin 6
# Key 3, pin 13
# Key 4, pin 19
# btn_one = Button(5) # assign btn_one to pin
# btn_one.when_pressed = handleBtnPress
# def handleBtnPress():
#     printToDisplay("Hello, world!")