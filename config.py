# Network
WIFI_SSID = "your SSID here!"
WIFI_PASS = "Your PSK here!"

heartbeat_interval = 300 # (seconds between connectivity tests)
heartbeat_url = "https://api.ipify.org"

# Relays
initial_values = {1: 1, 2: 1, 3: 0, 4: 0} # {relayid: value,...}
network_relay = 1 # ID of relay will reset on heartbeat failure