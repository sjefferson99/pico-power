from relay_board import relay_board
from machine import Pin
import network
import socket
import config
from time import sleep_ms

relays = relay_board()

led = Pin("LED", Pin.OUT)

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico-Power</title> </head>
    <body> <h1>Pico-Power: Relay control of 4 circuits up to 240v AC or 30v DC</h1>
        %s
    </body>
</html>
"""

baseurl_content = """
<p>
Use the following URL suffixes to drive functions on this Pico:
<ul>
<li>Relay control - <a href="relay">/relay</a></li>
</p>
"""

unknownurl_content = """
<p>
That URL hasn't been recognised.
</p>
"""

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
    while True:
        led.toggle()
        sleep_ms(100)
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

        baseurl = request.find('/ ')
        relayurl = request.find('/relay')
        
        if baseurl == 6:
            print("Base URL")
            content = baseurl_content

        elif relayurl == 6:
            print("Relay URL")
            content = relays.parse_web_request(request)

        else:
            print("Unknown URL")
            content = unknownurl_content + baseurl_content

        response = html % content

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')

#relays.demo()