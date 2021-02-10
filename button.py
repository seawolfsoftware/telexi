# Ctrl-c to end

print('LOAD: button.py')

import sys
import time
import machine


# def press():
#
#     print('Button PRESSED at:' )
#     time.sleep(5)
#
#
# led = machine.Pin(23, machine.Pin.OUT)
# button_state = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
#
# while True:
#     #  When a button is pressed, the corresponding pin is
#     #  connected to the ground and its value goes to 0
#     if button_state.value() == 0:
#         pass
#
#     elif button_state.value() == 1:
#         press()
#         led.on()
#         time.sleep(1)
#
# # The MIT License (MIT)
# # Copyright (c) 2020 Mike Teachman
# # https://opensource.org/licenses/MIT
#
# # Purpose:
# # - read 16-bit audio samples from a stereo formatted WAV file
# #   stored in the internal MicroPython filesystem
# # - write audio samples to an I2S amplifier or DAC module
# #
# # Sample WAV file in wav_files folder:
# #   "side-to-side-8k-16bits-stereo.wav"
# #
# # Hardware tested:
# # - PCM5102 stereo DAC module
# #
# # The WAV file will play continuously until a keyboard interrupt is detected or
# # the ESP32 is reset
#
# # from machine import I2S
# # from machine import Pin

# ======= USER CONFIGURATION =======
WAV_FILE = 'side-to-side-8k-16bits-stereo.wav'
SAMPLE_RATE_IN_HZ = 8000
# ======= USER CONFIGURATION =======


bck_pin = machine.Pin(26)
ws_pin = machine.Pin(25)
sdout_pin = machine.Pin(22)


# channelformat setting:
#     stereo WAV: channelformat=I2S.RIGHT_LEFT
audio_out = machine.I2S(
    machine.I2S.NUM1,
    bck=bck_pin,
    ws=ws_pin,
    sdout=sdout_pin,
    standard=machine.I2S.PHILIPS,
    mode=machine.I2S.MASTER_TX,
    dataformat=machine.I2S.B16,
    channelformat=machine.I2S.RIGHT_LEFT,
    samplerate=SAMPLE_RATE_IN_HZ,
    dmacount=10,
    dmalen=512)

wav = open(WAV_FILE, 'rb')

# advance to first byte of Data section in WAV file
pos = wav.seek(44)

# allocate sample arrays
#   memoryview used to reduce heap allocation in while loop
wav_samples = bytearray(2048)
wav_samples_mv = memoryview(wav_samples)

print('Starting')
# continuously read audio samples from the WAV file
# and write them to an I2S DAC
while True:
    try:
        num_read = wav.readinto(wav_samples_mv)
        num_written = 0
        # end of WAV file?
        if num_read == 0:
            # advance to first byte of Data section
            pos = wav.seek(44)
        else:
            # loop until all samples are written to the I2S peripheral
            while num_written < num_read:
                num_written += audio_out.write(wav_samples_mv[num_written:num_read], timeout=0)
    except (KeyboardInterrupt, Exception) as e:
        print('caught exception {} {}'.format(type(e).__name__, e))
        break

wav.close()
audio_out.deinit()
print('Done')
