# see https://www.lnrprecision.com/newstage/wp-content/uploads/2018/10/MTR-3B_LCD_user-manual_9_29_18.pdf on model


# data should include:
# current band: (160m, 80m, 40m, 30m, 20m, 17m, 15m, 12m, 10m, 6m, 2m, 70cm)
# current frequency (1.8, 3.5, 7, 10, 14, 18, 21, 24, 28, 50, 144, 430 MHz)
# morse code speed in WPM (words per minute)
# communication mode (USB, LSB, CW, FSK, AM, FM, Digital, etc.),
# current time, current battery voltage,
# RIT is on or off, and the amount of RIT

# current radio mode: (Operating, Direct Frequency Entry, Message Entry, Tune, Set Time, Config)

from enum import Enum
from datetime import datetime
from typing import Optional, Set, Callable

class Band(Enum):
    M160 = "160m"
    M80 = "80m"
    M40 = "40m"
    M30 = "30m"
    M20 = "20m"
    M17 = "17m"
    M15 = "15m"
    M12 = "12m"
    M10 = "10m"
    M6 = "6m"
    M2 = "2m"
    CM70 = "70cm"

QRP_CW_FREQUENCIES = {
    Band.M160: 1.810,
    Band.M80: 3.560,
    Band.M40: 7.030,
    Band.M30: 10.116,
    Band.M20: 14.060,
    Band.M17: 18.096,
    Band.M15: 21.060,
    Band.M12: 24.906,
    Band.M10: 28.060,
    Band.M6: 50.090,
    Band.M2: 144.207,
    Band.CM70: 432.060
}

class Mode(Enum):
    USB = "USB"
    LSB = "LSB"
    CW = "CW"
    FSK = "FSK"
    AM = "AM"
    FM = "FM"
    DIGITAL = "DIG"

# TODO: default band/mode frequencies
# TODO: cache last used frequency for each band/mode

class RadioMode(Enum):
    OPERATING = "Operating"
    DIRECT_FREQ_ENTRY = "Direct Frequency Entry"
    MESSAGE_ENTRY = "Message Entry"
    TUNE = "Tune"
    SET_TIME = "Set Time"
    CONFIG = "Config"

class Radio:
    def __init__(self):
        self.current_band: Band = Band.M20
        self.frequency: float = 14.060  # MHz
        self.wpm: int = 18
        self.mode: Mode = Mode.CW
        self.battery_voltage: float = 11.9
        self.rit_enabled: bool = False
        self.rit_offset: int = 0  # Hz
        self.radio_mode: RadioMode = RadioMode.OPERATING
        self._observers: Set[Callable] = set()

    @property
    def current_time(self) -> datetime:
        return datetime.now()

    def add_observer(self, observer: Callable[[], None]) -> None:
        """Add an observer that will be notified when radio state changes."""
        self._observers.add(observer)

    def remove_observer(self, observer: Callable[[], None]) -> None:
        """Remove an observer from the notification list."""
        self._observers.discard(observer)

    def _notify_observers(self) -> None:
        """Notify all observers that the radio state has changed."""
        for observer in self._observers:
            observer()

    def set_band(self, band: Band) -> None:
        self.current_band = band
        self.frequency = QRP_CW_FREQUENCIES[band]
        self._notify_observers()

    def change_band(self, direction: str) -> None:
        bands = list(Band)
        current_index = bands.index(self.current_band)
        if direction == "up":
            new_index = (current_index + 1) % len(bands)
        elif direction == "down":
            new_index = (current_index - 1) % len(bands)
        else:
            raise ValueError("Direction must be 'up' or 'down'")
        self.set_band(bands[new_index])

    def set_frequency(self, freq: float) -> None:
        self.frequency = round(freq, 4)
        # TODO: check frequency limits for the current band
        if self.current_band in QRP_CW_FREQUENCIES:
            QRP_CW_FREQUENCIES[self.current_band] = freq
        self._notify_observers()

    def increment_frequency(self, step: float) -> None:
        self.set_frequency(self.frequency + step)

    def set_wpm(self, wpm: int) -> None:
        self.wpm = max(5, min(50, wpm))  # Typical WPM range
        self._notify_observers()

    def set_mode(self, mode: Mode) -> None:
        self.mode = mode
        self._notify_observers()

    def set_radio_mode(self, mode: RadioMode) -> None:
        self.radio_mode = mode
        self._notify_observers()

    def toggle_rit(self) -> None:
        self.rit_enabled = not self.rit_enabled
        self._notify_observers()

    def set_rit_offset(self, offset: int) -> None:
        self.rit_offset = max(-9999, min(9999, offset))  # Typical RIT range
        self._notify_observers()

    def update_battery_voltage(self, voltage: float) -> None:
        self.battery_voltage = voltage
        self._notify_observers()

    def get_state(self) -> dict:
        return {
            "band": self.current_band.value,
            "frequency": self.frequency,
            "wpm": self.wpm,
            "mode": self.mode.value,
            "time": self.current_time.strftime("%H:%M:%S"),
            "battery": self.battery_voltage,
            "rit_enabled": self.rit_enabled,
            "rit_offset": self.rit_offset,
            "radio_mode": self.radio_mode.value
        }


