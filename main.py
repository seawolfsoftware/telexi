print('Running: main.py')

import button

button.press()

from machine import Pin
from time import sleep

print('Entering main program...~~~~~')

led = Pin(23, Pin.OUT)
button = Pin(22, Pin.IN)

while True:

    button_state = button.value()
    if button_state == True:
        led.value(1)
    else:
        led.value(0)



from machine import Pin
led = Pin(12, Pin.OUT)  # IO16
led2 = Pin(5, Pin.OUT)


