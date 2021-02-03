# This file is executed on every boot (including wake-boot from deepsleep)

print('Running: boot.py')


import network
import sys


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to Wi-Fi...')
    wlan.connect('Chaz&Annie', 'Watermelon23')
    while not wlan.isconnected():
        pass
print('Network configuration:', wlan.ifconfig())
