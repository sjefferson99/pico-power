import network
from time import sleep_ms
import config
from machine import Pin
import urequests
import uasyncio as asyncio
from relays.hardware import relay_board

class wireless:
    """
    Sets up and manages wifi connection
    """    
    def __init__(self) -> None:
        self.test_result = False
        self.heartbeat_interval = config.heartbeat_interval
        self.heartbeat_url = config.heartbeat_url
        self.network_relay = config.network_relay

        self.led = Pin("LED", Pin.OUT)

    def start_wifi(self) -> bool:
        print("Attempting wifi connection")
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(config.WIFI_SSID, config.WIFI_PASS)

        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            self.led.toggle()
            sleep_ms(500)

        if self.wlan.status() != 3:
            error_wait = 100
            while error_wait > 0:
                self.led.toggle()
                sleep_ms(100)
                error_wait -= 1
            return False
                
        else:
            print('connected')
            status = self.wlan.ifconfig()
            print( 'ip = ' + str(status[0]))
            return True
    
    def wireless_status(self) -> int:
        return self.wlan.status()

    def reset_network(self):
        # TODO have a 0 option for no network relay and fall back to regular
        #  testing only
        print("Resetting network relay")
        hardware = relay_board()
        hardware.relay_toggle(self.network_relay, 4000, 0)
        
        connected = False
        while connected == False:
            connected = self.start_wifi()

    async def test_request(self) -> bool:
        """
        Attempt to connect to a known high uptime website. If urequest
        connection error, reset the network relay and run the wifi connect
        function until reconnected, retest after test interval and repeat until
        test successful.
        """
        while True:
            print("Test executing")
            try:
                print("Testing...")
                res = urequests.get(url=self.heartbeat_url)
                print("Return code {} - Content: {}".format(res.status_code, res.text))
                res.close()
                self.test_result = True
                print("Connectivity OK")
        
            except Exception as e:
                print("Connectivity issue: {}".format(e))
                self.test_result = False
                print("Connectivity error... resetting network")
                self.reset_network()

            await asyncio.sleep(self.heartbeat_interval)