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

#init LED
led = Pin("LED", Pin.OUT)
led.on()
sleep_ms(50)
led.off()

#init vars
rundemo = False

def relay_on_off(relay: Pin, duration_ms: int = 1000):
    """Connects common to NO for specified duration in ms then reverts to common connected to NC"""
    relay.value(1)
    sleep_ms(duration_ms)
    relay.value(0)

def relay_off_on(relay: Pin, duration_ms: int = 1000):
    """Connects common to NC for specified duration in ms then reverts to common connected to NO"""
    relay.value(0)
    sleep_ms(duration_ms)
    relay.value(1)

def demo():
    x = 0
    while x < 10:
        led.on()
        sleep_ms(100)
        led.off()
        sleep_ms(100)
        x += 1
    
    for relay in relays:
        relay_on_off(relay)
        sleep_ms(500)

if rundemo:
    demo()
    