from utime import sleep_ms
from machine import Pin

class relay_board:
    """
    Creates abstraction for the pi hut 4 opto relay board for Pico W - Maps relays to GP18-21.
    Extends base tinyweb server with relay functionality
    Execute demo() for a board self test
    """
    def __init__(self) -> None:
        self.pin_mapping = {1: 18, 2: 19, 3: 20, 4: 21}
        self.relays = {}
        self.states = {0: "off", 1: "on"}
        #Build pin objects
        x = 1
        p = 18
        while x <= 4:
            self.relays[x] = Pin(p, Pin.OUT)
            x += 1
            p += 1
        
    def relay_toggle(self, relay: int, duration_ms: int = 1000, initial_value: int=1) -> None:
        """For specified relay, connects common to intiial value terminal for specified duration in ms then toggles to the opposite terminal
        Initial value:
        1: Common connected to NO
        0: Common connected to NC
        """
        print("Toggling relay: " + str(relay) + " to value: " + str(initial_value) + " for duration: " + str(duration_ms))
        self.relays[relay].value(initial_value)
        sleep_ms(duration_ms)
        self.relays[relay].toggle()

    def relay_switch(self, relay: int, value: int=1) -> None:
        """For specified relay, connects common to value terminal
        Value:
        1: Common connected to NO
        0: Common connected to NC
        """
        print("Switching relay: " + str(relay) + " to value: " + str(value))
        self.relays[relay].value(value)

    def list_relays(self) -> list:
        x = 1
        relaylist = []
        while x <= 4:
            relaylist.append([x, "Relay " + str(x)]) #Generate some names for illustrative purposes
            x += 1
        return relaylist

    def demo(self) -> None:
        """Cycles quickly through toggling each relay"""
        x = 1
        while x <= 4:
            self.relay_switch(x, 1)
            sleep_ms(200)
            x += 1
        x = 1
        while x <= 4:
            self.relay_switch(x, 0)
            sleep_ms(200)
            x += 1
        x = 1
        while x <= 4:
            self.relay_toggle(x, 100, 1)
            sleep_ms(200)
            x += 1