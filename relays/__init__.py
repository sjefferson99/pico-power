from webserver import website
from webpages import relaysite
from api import relayapi
from hardware import relay_board

class relay_module:
    """
    Creates abstraction for the pi hut 4 opto relay board for Pico W - Maps relays to GP18-21.
    Extends base tinyweb server with relay functionality
    Execute demo() for a board self test
    """
    def __init__(self) -> None:
        """
        Hardware setup
        """    
        self.hardware = relay_board()

    def create_relay_website(self, coresite: website) -> None:
        """
        Tinyweb server definitions for the relay board to extend the webserver passed.
        """
        print("Building relay API website elements")
        api = relayapi(coresite)
        print("Building relay content website elements")
        site = relaysite(coresite)