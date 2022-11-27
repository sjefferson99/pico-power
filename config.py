# Network
WIFI_SSID = "your SSID here!"
WIFI_PASS = "Your PSK here!"

## (seconds between connectivity tests), enter 0 to disable
heartbeat_interval = 300
## URL for heartbeat test - pick a high uptime site that returns http 200
heartbeat_url = "https://api.ipify.org"

# Relays
## {relayid: value,...}
initial_values = {1: 1, 2: 1, 3: 0, 4: 0}
## ID of relay will reset on heartbeat failure, enter 0 for no relay
network_relay = 1
## Duration in ms for network relay to remain off on failed test reset
reset_duration = 4000