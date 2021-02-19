#
#   The MIT License (MIT)
#
#   Copyright (c) 2021 Jej (@GitHub / https://github.com/jej/micropython-interact)
#
#   https://opensource.org/licenses/MIT
#

from machine import Pin, Timer
from time import ticks_diff, ticks_ms


class Interact:
    """
        Interact class
            A MicroPython library to manage switches and capacitive touch.

            https://github.com/jej/micropython-interact
    """

    def __init__(self,
                 pin,
                 **kwargs
                 ):

        self.kwargs = kwargs
        self.pin = pin
        self._irq = kwargs.get('irq', True)
        self._dcd_ms = kwargs.get('debounce_check_delay_ms', 5)
        self._dcc = kwargs.get('debounce_checks_count', 3)
        self._pull = kwargs.get('pulled_up', True)
        self.touch_sensitivity = kwargs.get('touch_sensitivity', -1)
        if self.touch_sensitivity >= 0:
            self._irq = False

        self._longpress_timer = Timer(-1)
        self._smartclicks_timer = Timer(-1)
        self._debounce_timer = Timer(-1)
        self._debounce_counter = self._click_time_ms = self._smartclick_time_ms = 0
        self._rise_fall_check = self._debounced_value = self._smartclick_count = self._value = 1

        for k in ['irq', 'debounce_check_delay_ms', 'debounce_checks_count', 'pulled_up', 'touch_sensitivity']:
            self.kwargs.pop(k, None)

        self._enable_switch_irq()

    # IRQ emulation
    def update(self):
        self._value = self._get_pin_value()
        if self._rise_fall_check != self._value:
            self._rise_fall_check = self._value
            self._start_debouncing_timer()

    # Get logical sensor state
    def value(self):
        if self._pull:
            return 1 - self._debounced_value
        else:
            return self._debounced_value

    # Stop sensor
    def deinit(self):
        if self._irq:
            self.pin.irq(trigger=0, handler=None)

        self._debounce_timer.deinit()
        self._longpress_timer.deinit()
        self._smartclicks_timer.deinit()

    # Restart sensor
    def init(self):
        self._enable_switch_irq()

    ## /!\ Private methods ##

    def _enable_switch_irq(self):
        if self._irq:
            self.pin.irq(handler=self._switch_irq_handler, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

    def _switch_irq_handler(self, pin):
        pin.irq(trigger=0, handler=None)
        self._value = pin.value()
        self._debounce_counter = 0
        self._start_debouncing_timer()

    def _get_pin_value(self):
        if self.touch_sensitivity >= 0:
            return 1 if self.pin.read() > self.touch_sensitivity else 0
        else:
            return self.pin.value()

    def _start_debouncing_timer(self):
        self._debounce_timer.init(
            period=self._dcd_ms,  # debounce_check_delay_ms
            mode=Timer.ONE_SHOT,
            callback=self._debounce_callback
        )

    def _trigger(self, event, arg=None):
        if event in self.kwargs:
            if arg is None:
                self.kwargs[event]()
            else:
                self.kwargs[event](arg)
        elif 'callback' in self.kwargs:
            self.kwargs['callback'](event, arg)

    def _debounce_callback(self, _):
        bounce_value = self._get_pin_value()

        if bounce_value != self._value:
            # Bouncing
            self._value = bounce_value
            self._debounce_counter = 0
            self._start_debouncing_timer()
        else:
            self._debounce_counter += 1

            if self._debounce_counter < self._dcc:  # debounce_checks_count
                self._start_debouncing_timer()
            else:
                # Debounced
                if self._debounced_value != self._value:
                    self._debounced_value = self._value

                    lpd_ms = self.kwargs.get('longpress_delay_ms', 880)
                    t = ticks_ms()

                    if self.value():
                        # Pressed
                        self._click_time_ms = t
                        self._smartclicks_timer.deinit()
                        self._trigger('pressed')
                        self._longpress_timer.init(
                            period=lpd_ms,  # longpress_delay_ms
                            mode=Timer.ONE_SHOT,
                            callback=lambda _: self._trigger('longpressed')
                        )
                    else:
                        # Released
                        self._longpress_timer.deinit()
                        self._trigger('released')

                        since_click_ms = ticks_diff(t, self._click_time_ms)

                        if since_click_ms <= self.kwargs.get('click_delay_ms', 440):
                            # Clicked
                            scd_ms = self.kwargs.get('smartclick_delay_ms', 440)

                            if (ticks_diff(t, self._smartclick_time_ms) < scd_ms):  # smartclick_delay_ms
                                self._smartclick_count += 1
                            else:
                                self._smartclick_count = 1

                            self._smartclick_time_ms = t

                            self._trigger('clicked', self._smartclick_count)

                            # Timer for smartclicked callback call
                            self._smartclicks_timer.init(
                                period=scd_ms,  # smartclick_delay_ms
                                mode=Timer.ONE_SHOT,
                                callback=lambda _: self._trigger('smartclicked', self._smartclick_count)
                            )

                        elif since_click_ms >= lpd_ms:  # longpress_delay_ms
                            self._trigger('longclicked')

                # Next round
                self._enable_switch_irq()
