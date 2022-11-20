import sys
sys.path.append('/relays')
sys.path.append('/tinyweb')

import config
import network
from relays import relay_module
from webserver import website
from machine import Pin
from time import sleep_ms

def start_wifi() -> bool:
    print("Attempting wifi connection")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config.WIFI_SSID, config.WIFI_PASS)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        led.on()
        sleep_ms(500)
        led.off()
        sleep_ms(500)

    if wlan.status() != 3:
        error_wait = 100
        while error_wait > 0:
            led.toggle()
            sleep_ms(100)
            error_wait -= 1
        return False
            
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
        return True

# Enable webserver option (disable if relay module to be addressed via I2C on boatman network)
enable_webserver = True

print("Configuring LED")
led = Pin("LED", Pin.OUT)

# Load relay hardware
print("Enabling relay hardware")
relays = relay_module()
hardware = relays.hardware
print("Running hardware demo")
#hardware.demo()

if enable_webserver:
    # Instantiate wifi
    print("Wifi enabled - Connecting to wifi")
    connected = False
    while connected == False:
        connected = start_wifi()       

    # Instantiate core website
    print("Webserver enabled - Building core site")
    picoserver = website()
    
    # Create relay website elements
    print("Building relay website elements")
    relays.create_relay_website(picoserver)

    # Load the webserver
    print("Starting web server")
    picoserver.run()