import sys
sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys

from lib import epd2in7_V2

from PIL import Image, ImageDraw, ImageFont
import time
import os
from gpiozero import Button
from signal import pause

RUNNING = True

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
    print("Program starting...") # prints to console, not the display, for debugging

    key_1 = Button(5)                              # assign each button to a variable
    key_2 = Button(6)                              # by passing in the pin number
    key_3 = Button(13)
    key_4 = Button(19)                             # associated with the button 
    
    epd = epd2in7_V2.EPD() # get the display
    epd.init()           # initialize the display
    print("writing to e-Paper display...") # prints to console, not the display, for debugging
    printToDisplay("Button Demo\nPress ALL Keys\nto quit") # prints to the display

    # TODO: vanity splash screen

    # pause() # wait for button presses

    while RUNNING:
        if key_1.is_pressed and key_2.is_pressed and key_3.is_pressed and key_4.is_pressed:
            print("ALL Keys Pressed!\nSTOPPING") # prints to console, not the display, for debugging
            printToDisplay("All Keys Pressed!\nSTOPPING")
            time.sleep(1)
            epd.Clear()        # corrected method call
            epd.sleep()        # put the display to sleep
            RUNNING = False
        else:
            # clear the terminal console before printing
            os.system('clear')

            # create a message that gives the status of the buttons being pushed or not
            message = "Button 1: {}\nButton 2: {}\nButton 3: {}\nButton 4: {}".format(
                key_1.is_pressed, key_2.is_pressed, key_3.is_pressed, key_4.is_pressed)
            print(message)

            # printToDisplay(message) # prints to the display
            time.sleep(0.1)

    # epd.Clear()        # corrected method call
    # epd.sleep()        # put the display to sleep
