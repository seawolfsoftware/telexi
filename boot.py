import json
import network
import socket
import time
from Interact import *
from machine import Pin, TouchPad

# Read config file from file system into json object
with open('config.json') as f:
    config = json.load(f)


# Check config.json has updated credentials
if config['ssid'] == '' or None:
    assert False, 'config.json ssid value is empty'
elif config['ssid_password'] == '' or None:
    assert False, 'config.json ssid password value is empty'


def connect_to_wifi():

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wifi ...')
        wlan.connect(config['ssid'], config['ssid_password'])

        while not wlan.isconnected():
            pass
    print('Network Configuration:', wlan.ifconfig())


def start_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        # Socket accept()
        conn, addr = s.accept()
        print("Got connection from %s" % str(addr))

        # Socket receive()
        request = conn.recv(1024)
        print("")
        print("")
        print("Content %s" % str(request))

        # Socket send()
        request = str(request)
        # led_on = request.find('/?LED=1')
        # led_off = request.find('/?LED=0')
        # if led_on == 6:
        #     print('LED ON')
        #     print(str(led_on))
        #     led.value(1)
        # elif led_off == 6:
        #     print('LED OFF')
        #     print(str(led_off))
        #     led.value(0)
        response = web_page()

        conn.send(bytes('HTTP/1.1 200 OK\n', 'utf-8'))
        conn.send(bytes('Content-Type: text/html\n', 'utf-8'))
        conn.send(bytes('Connection: close\n\n', 'utf-8'))
        conn.sendall(response)

        # Socket close()
        conn.close()


def web_page():
    html_page = """  
            <html>  
            <head>  
              <meta content="width=device-width, initial-scale=1" name="viewport"></meta>  
            </head>  
            <body>  
                <h1>telexi</h1>
            </body>  
            </html>"""
    return html_page


def connect_to_upstream_socket():

    url = config['server_url']
    _, _, host, path = url.split('/', 3)

    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = socket.getaddrinfo(config['server_ip'], 80)[0][-1]
        print('Socket address is:', addr)

        # Connect to upstream socket
        s.connect(addr)

        my_touch = Interact(TouchPad(Pin(14)),
                            touch_sensitivity=250,
                            callback=lambda event, clicks: print(event, clicks))

        # Listen for touch events every 10ms
        while True:
            my_touch.update()
            print(my_touch.value())
            # if my_touch.value() == 1:
            #     print('dat touch')
                # request = bytes("GET /api/v1/ HTTP/1.1\r\nHost: telexi.seawolfsoftware.io\r\n\r\n", 'utf-8')
                # # request = b"".join([method])
                # s.send(request)
                #
                # data = s.recv(1024)
                # time.sleep(1)
                #
                # if data:
                #     print(str(data, 'utf8'), end='')
                # else:
                #     continue
                # s.close()
            # time.sleep(1)


def post_event_to_api():

    url = config['server_url']
    _, _, host, path = url.split('/', 3)

    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = socket.getaddrinfo(config['server_ip'], 80)[0][-1]
        print('Socket address is:', addr)

        # Connect to upstream socket
        s.connect(addr)

        method = bytes('POST /', 'utf-8')
        path = bytes('api/v1/ ', 'utf-8')
        protocol = bytes('HTTP/1.1\r\n', 'utf-8')
        host = bytes("Host: telexi.seawolfsoftware.io\r\n", 'utf-8')
        content_type = bytes('Content-Type: application/json\r\n', 'utf-8')

        # convert json string to binary
        body_dict = '{"device_id":"gdd", "is_button_on": "true"}\r\n'
        raw_content_length = 'Content-Length: ' + str(len(body_dict)) + '\r\n\r\n'
        content_length = bytes(raw_content_length, 'utf-8')
        binary_body = bytes(body_dict, 'utf-8')

        # Build binary request
        request = b"".join([method,
                            path,
                            protocol,
                            host,
                            content_type,
                            content_length,
                            binary_body])

        # Send request to endpoint
        s.send(request)

        # Read response into buffer
        data = s.recv(1024)
        time.sleep(3)

        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
        s.close()


# connect_to_wifi()
# connect_to_upstream_socket()


# Ctrl-c to end

print('LOAD: audio.py')

import sys
import time
import machine

"""
    - read 16-bit audio samples from a stereo formatted WAV file
      stored in the internal MicroPython filesystem
    - write audio samples to an I2S amplifier or DAC module

    Hardware tested:
    - PCM5102 stereo DAC module

    WAV file will play continuously until a keyboard interrupt or esp32 reset

"""

WAV_FILE = 'beat.wav'
SAMPLE_RATE_IN_HZ = 44100

bck_pin = machine.Pin(26)
ws_pin = machine.Pin(25)
sdout_pin = machine.Pin(22)

#  channelformat setting:
#  stereo WAV: channelformat=I2S.RIGHT_LEFT
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
