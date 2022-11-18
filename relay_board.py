from utime import sleep_ms
from machine import Pin

class relay_board:
    """
    Creates abstraction for the pi hut 4 opto relay board for Pico W - Maps relays to GP18-21.
    Execute demo() for a board self test
    """
    def __init__(self) -> None:
        self.pin_mapping = {1: 18, 2: 19, 3: 20, 4: 21}
        self.relays = {}
        #Build pin objects and set known state (off)
        x = 1
        p = 18
        while x <= 4:
            self.relays[x] = Pin(p, Pin.OUT)
            self.relays[x].value(0) #set NO to off
            x += 1
            p += 1

    def relay_toggle(self, relay: int, duration_ms: int = 1000, initial_value: int=1) -> None:
        """For specified relay, connects common to intiial value terminal for specified duration in ms then toggles to the opposite terminal
        Initial value:
        1: Common connected to NO
        0: Common connected to NC
        """
        self.relays[relay].value(initial_value)
        sleep_ms(duration_ms)
        self.relays[relay].toggle()

    def demo(self) -> None:
    
        x = 1
        while x <= 4:
            self.relay_toggle(x, 100, 1)
            sleep_ms(200)
            x += 1