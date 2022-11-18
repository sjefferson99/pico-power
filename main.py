from relay_board import relay_board
from machine import Pin
import network
import socket
import config
import time

relays = relay_board()

led = Pin("LED", Pin.OUT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config.WIFI_SSID, config.WIFI_PASS)

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W</h1>
        <p>%s</p>
    </body>
</html>
"""

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        toggle_on = request.find('/toggle/on')
        toggle_off = request.find('/toggle/off')
        print( 'toggle on = ' + str(toggle_on))
        print( 'toggle off = ' + str(toggle_off))

        if toggle_on == 6:
            print("Toggling on")
            relays.relay_toggle(4,500,1)
            stateis = "Toggling on"

        if toggle_off == 6:
            print("Toggling off")
            relays.relay_toggle(4,500,0)
            stateis = "Toggling off"

        response = html % stateis

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')

#relays.demo()