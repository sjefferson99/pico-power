from utime import sleep_ms
from machine import Pin

#init relays
relay1 = Pin(18, Pin.OUT)
relay1.value(0) #Ensure power on
relay2 = Pin(19, Pin.OUT)
relay2.value(0) #Ensure power on
relay3 = Pin(20, Pin.OUT)
relay3.value(0) #Ensure power on
relay4 = Pin(21, Pin.OUT)
relay4.value(0) #Ensure power on

relays = [relay1, relay2, relay3, relay4]

def interrupt_power(relay, ms=1000):
    relay.value(1) # Disconnect power
    sleep_ms(ms)
    relay.value(0) # Reconnect power

for relay in relays:
    interrupt_power(relay)
    sleep_ms(500)

#interrupt_power(relays[3])