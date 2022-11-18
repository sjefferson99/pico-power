from utime import sleep_ms
from machine import Pin

class relay_board:
    """
    Creates abstraction for the pi hut 4 opto relay board for Pico W - Maps relays to GP18-21.
    Provides URL parsing and content for a webserver
    Execute demo() for a board self test
    """
    def __init__(self) -> None:
        self.pin_mapping = {1: 18, 2: 19, 3: 20, 4: 21}
        self.relays = {}
        self.states = {0: "off", 1: "on"}
        #Build pin objects and set known state (off)
        x = 1
        p = 18
        while x <= 4:
            self.relays[x] = Pin(p, Pin.OUT)
            self.relays[x].value(0) #set NO to off
            x += 1
            p += 1
        
        self.base_relay_content = """
            <p>
            Use the following endpoints to drive the pico relays:
            <ul>
            <li>Switch relay on (NO switched to common) - /relay/switch/{relay number (1-4)}/on</li>
            <li>Switch relay off (NC switched to common) - /relay/switch/{relay number (1-4)}/off/</li>
            <li>Toggle relay on (NO switched to common) then off with a specified duration period - /relay/toggle/{relay number (1-4)}/on/{xxxx - duration in ms (must be 4 digits)}</li>
            <li>Toggle relay off (NC switched to common) then on with a specified duration period - /relay/toggle/{relay number (1-4)}/off/{xxxx - duration in ms (must be 4 digits)}</li>
            </p>
            """
        self.unknown_url_content = """
        <p>
        That URL is not recognised.
        </p>
        """
        
    def relay_toggle(self, relay: int, duration_ms: int = 1000, initial_value: int=1) -> None:
        """For specified relay, connects common to intiial value terminal for specified duration in ms then toggles to the opposite terminal
        Initial value:
        1: Common connected to NO
        0: Common connected to NC
        """
        self.relays[relay].value(initial_value)
        sleep_ms(duration_ms)
        self.relays[relay].toggle()

    def relay_switch(self, relay: int, value: int=1) -> None:
        """For specified relay, connects common to value terminal
        Value:
        1: Common connected to NO
        0: Common connected to NC
        """
        self.relays[relay].value(value)

    def demo(self) -> None:
        """Cycles quickly through toggling each relay"""
        x = 1
        while x <= 4:
            self.relay_toggle(x, 100, 1)
            sleep_ms(200)
            x += 1
    
    def parse_web_request(self, request_data: str) -> str:
        """Takes web request data from a client determined to be in the
        "/relay" page space, parses the request data, executes any appropriate
        relay actions and returns the appropriate content to serve to the web
        client"""
        
        relay_url = request_data.find('/relay ')
        action_relay_url = request_data.find('/relay/')

        if relay_url == 6:
            print("Relay base URL")
            content = self.base_relay_content

        elif action_relay_url == 6:
            print("Relay action URL")
            
            relay_number = int(request_data[20:21])
            on_off = request_data[22:24]
            if on_off == "on":
                state = 1
            else:
                state = 0

            if request_data[13:19] == "switch":
                content = "Switching relay " + str(relay_number) + " " + self.states[state]
                print(content)
                self.relay_switch(relay_number, state)

            elif request_data[13:19] == "toggle":
                if state == 0:
                    duration = int(request_data[26:30])
                else:
                    duration = int(request_data[25:29])
                content = "Toggling relay " + str(relay_number) + " " + self.states[state] + " for " + str(duration) + " ms"
                print(content)
                self.relay_toggle(relay_number, duration, state)
            
            else:
                content = "Unknown relay URL " + request_data[13:19]
                print(content)

        else:
            print("Unknown relay URL")
            content = self.unknown_url_content + self.base_relay_content

        return content