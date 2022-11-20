import sys
sys.path.append('/relays')
sys.path.append('/tinyweb')

import config
from relays import relay_module
from networking import wireless
from webserver import website
from machine import Pin

# Enable webserver option (disable if relay module to be addressed via I2C on boatman network)
enable_networking = True
enable_webserver = True

print("Configuring LED")
led = Pin("LED", Pin.OUT)

# Load relay hardware
print("Enabling relay hardware")
relays = relay_module()
hardware = relays.hardware
# Set initial relay states
initial_values = config.initial_values
for relay in initial_values:
    hardware.relay_switch(relay, initial_values[relay])

#print("Running hardware demo")
#hardware.demo()

if enable_networking:
    # Instantiate wifi
    print("Wifi enabled - Connecting to wifi")
    wifi = wireless()
    connected = False
    while connected == False:
        connected = wifi.start_wifi(led)

if enable_webserver:
    if not enable_networking:
        print("Website needs networking, but networking is disabled - skipping website")
    
    else:
        # Instantiate core website
        print("Webserver enabled - Building core site")
        picoserver = website()
        
        # Create relay website elements
        print("Building relay website elements")
        relays.create_relay_website(picoserver)

        # Load the webserver
        print("Starting web server")
        picoserver.run()