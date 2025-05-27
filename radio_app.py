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

def main():
    global epd
    
    # Initialize components
    button_manager = ButtonStateManager([5, 6, 13, 19])
    radio = Radio()
    epd = epd2in7_V2.EPD() # get the display
    epd.Init_4Gray()           # initialize the display
    display = RadioDisplay(radio, epd)  # Pass epd to RadioDisplay
    command_handler = RadioCommandHandler(radio)

    display.Splash()  # Show splash screen
    display.update_display()  # Update the display with initial radio status

    while True:
        button_states = button_manager.get_button_states()
        
        # Check for exit condition
        if all(button_states):
            print("\nALL Keys Pressed!\nSTOPPING") # prints to console, not the display, for debugging
            display.QRT()  # QRT on the display
            break
        
        os.system('clear')  # clear the terminal console before printing

        # print radio time
        print("Current Time: {}".format(radio.current_time.strftime("%H:%M:%S")))

        # print current radio status
        print("Current Band: {}\nFrequency: {:.4f} MHz\nWPM: {}\nMode: {}\nBattery Voltage: {}\nRIT: {}\nRIT Offset: {}\nRadio Mode: {}".format(
            radio.current_band.value, radio.frequency, radio.wpm, radio.mode.value, radio.battery_voltage, radio.rit_enabled, radio.rit_offset, radio.radio_mode.value))

        # create a message that gives the status of the buttons being pushed or not
        message = "\nButton 1: {}\nButton 2: {}\nButton 3: {}\nButton 4: {}\n".format(
            button_states[0], button_states[1], button_states[2], button_states[3])
        print(message)

        time.sleep(0.1)

        # Handle button states
        command_handler.handle_button_state(ButtonState(button_states))
        # observer pattern handles display updates

if __name__ == '__main__':
    main()