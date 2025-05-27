from enum import Enum
from typing import List, Dict
from radio import Radio, RadioMode

class ButtonState:
    def __init__(self, button_states: List[bool]):
        self.states = button_states

    def __str__(self):
        return f"Buttons: {self.states}"

class RadioCommandHandler:
    def __init__(self, radio: Radio):
        self.radio = radio
        self._command_map: Dict = self._init_command_map()

    def _init_command_map(self) -> Dict:
        return {
            # TODO: Add more button combinations and their corresponding commands
            (True, False, False, False): self._function_key,
            (False, True, False, False): self._km_rit,
            (False, False, True, False): self._increment_frequency,
            (False, False, False, True): self._decrement_frequency,
            (True, True, False, False): self._band_up,
            (False, False, True, True): self._band_down,
        }

    def handle_button_state(self, button_state: ButtonState) -> None:
        # Convert button state to tuple for mapping
        state_tuple = tuple(button_state.states)
        
        if state_tuple in self._command_map:
            command = self._command_map[state_tuple]
            command()

    def _function_key(self):
        # TODO: Implement function key behavior
        pass

    def _km_rit(self):
        # TODO: long and short press need to be handled
        pass

    def _increment_frequency(self):
        self.radio.increment_frequency(0.0005)

    def _decrement_frequency(self):
        self.radio.increment_frequency(-0.0005)

    def _band_up(self):
        self.radio.change_band("up")

    def _band_down(self):
        self.radio.change_band("down")