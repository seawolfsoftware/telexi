# Ctrl-c to end

print('LOAD: button.py')

import sys
import time
import machine


def press():
    print('Button PRESSED.')


led = machine.Pin(23, machine.Pin.OUT)
button_state = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    #  When a button is pressed, the corresponding pin is
    #  connected to the ground and its value goes to 0
    if button_state.value() == 0:
        press()
        led.on()

    elif button_state.value() == 1:
        pass