import network
from time import sleep_ms
import config
from machine import Pin
import urequests

class wireless:
    """
    Sets up and manages wifi connection
    """    
    def __init__(self) -> None:
        self.network_relay = 1

    def start_wifi(self, led: Pin) -> bool:
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
            led.on()
            sleep_ms(500)
            led.off()
            sleep_ms(500)

        if self.wlan.status() != 3:
            error_wait = 100
            while error_wait > 0:
                led.toggle()
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

    def test_request(self) -> bool:
        try:
            print("Pinging...")
            res = urequests.get(url='https://api.ipify.org')
            print("Return code {} - Content: {}".format(res.status_code, res.text))
            res.close()
            self.result = True
    
        except Exception as e:
            print("Connectivity issue: {}".format(e))
            self.result = False

        return self.result