from gpiozero import Button
from typing import List

class ButtonStateManager:
    def __init__(self, pin_numbers: List[int]):
        self.buttons = [Button(pin) for pin in pin_numbers]

    def get_button_states(self) -> List[bool]:
        return [button.is_pressed for button in self.buttons]