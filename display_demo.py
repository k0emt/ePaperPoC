import os
import sys
import time
from signal import pause

from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont

from lib import epd2in7_V2
from radio import Radio
from radio_command_handler import RadioCommandHandler, ButtonState
from button_state_manager import ButtonStateManager
from radio_display import RadioDisplay

global epd

sys.path.insert(1, "./lib")

# this code is used for developing the display code

def main():
    global epd
    
    # Initialize components
    radio = Radio()
    epd = epd2in7_V2.EPD() # get the display
    epd.Init_4Gray()           # initialize the display
    display = RadioDisplay(radio, epd)  # Pass epd to RadioDisplay
    command_handler = RadioCommandHandler(radio)

    display.Splash()  # Show splash screen

    # print radio time
    print("Current Time: {}".format(radio.current_time.strftime("%H:%M:%S")))

    # print current radio status
    print("Current Band: {}\nFrequency: {:.4f} MHz\nWPM: {}\nMode: {}\nBattery Voltage: {}\nRIT: {}\nRIT Offset: {}\nRadio Mode: {}".format(
            radio.current_band.value, radio.frequency, radio.wpm, radio.mode.value, radio.battery_voltage, radio.rit_enabled, radio.rit_offset, radio.radio_mode.value))

    display.update_display()
    time.sleep(4)

    display.QRT()  # Show QRT screen
    display.clearSleep() # clear the screen and put the display to sleep

if __name__ == '__main__':
    main()