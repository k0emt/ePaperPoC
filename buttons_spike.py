import sys
sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys

from lib import epd2in7_V2

from PIL import Image, ImageDraw, ImageFont
import time
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

def handleBtnPress(btn):
    global RUNNING

    # get the button pin number
    pinNum = btn.pin.number
    
    # python hack for a switch statement. The number represents the pin number and
    # the value is the message we will print
    switcher = {
        5: "Button 1\nHello, World!",
        6: "Button 2\nThis is my first \nRPi project.",
        13: "Button 3\nHope you liked it.",
        19: "Button 4\nGoodbye"
    }
    
    # get the string based on the passed in button and send it to printToDisplay()
    msg = switcher.get(btn.pin.number, "Error")
    printToDisplay(msg)

    # if the button pin number is 19 then clear the display and sleep and quit
    if pinNum == 19:
        print("clearing display...")
        epd.Clear()        # corrected method call
        epd.sleep()        # put the display to sleep
        print("quitting...")
        RUNNING = False

# main program

if __name__ == '__main__':
    print("Program start...") # prints to console, not the display, for debugging

    btn1 = Button(5)                              # assign each button to a variable
    btn2 = Button(6)                              # by passing in the pin number
    btn3 = Button(13)
    btn4 = Button(19)                             # associated with the button 
    
    btn1.when_pressed = handleBtnPress
    btn2.when_pressed = handleBtnPress
    btn3.when_pressed = handleBtnPress
    btn4.when_pressed = handleBtnPress

    epd = epd2in7_V2.EPD() # get the display
    epd.init()           # initialize the display
    print("writing to e-Paper display...") # prints to console, not the display, for debugging
    printToDisplay("Button Demo\nPress a button!") # prints to the display

    # pause() # wait for button presses

    while RUNNING:
        time.sleep(0.1)

    # epd.Clear()        # corrected method call
    # epd.sleep()        # put the display to sleep

# from gpiozero import Button
# Key 1, pin 5
# Key 2, pin 6
# Key 3, pin 13
# Key 4, pin 19