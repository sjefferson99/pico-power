# Pico-Power

## Introduction

Pico W based relay controller for web based control of DC and AC circuits onboard.

This code is built around the Pimoroni Pico W firmware v1.19.9: https://github.com/pimoroni/pimoroni-pico/releases/download/v1.19.9/pimoroni-picow-v1.19.9-micropython.uf2

## Hardware
- Uses Pico W board mounted on the PiHut relay board: https://thepihut.com/products/raspberry-pi-pico-relay-board

- Optional LiPo and charger shim allows the Pico to reset circuits it is powered by without shutting down, you will need to connect VSYS to VBUS to power the relays from the shim.
  - Battery: https://thepihut.com/products/2000mah-3-7v-lipo-battery?variant=42143258050755
  - Charging shim: https://thepihut.com/products/lipo-shim-for-pico?variant=39809509785795

## Usage
- Populate wifi SSID and password in the config.py file
- Determine pico IP from DHCP server (hostname appears to be "PYBD")
- Navigate to http://<pico IP>:80 for further instructions

### LED behaviour
#### Board power
The board has a power LED to show that the Pico AND the relay board have power ie 5v on VBUS as opposed to just VSYS
#### Relay state
The relays each have an LED to show relay state on/off
#### Pico LED
The Pico LED is normally off in proper operation.

When connecting to the wifi the LED will flash once per second. Should the conection fail, the LED will flash 5 times per second for the retry backoff period then loop back to connecting.