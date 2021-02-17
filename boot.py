import json
import time
import network
import urequests
import socket
import os

# Read config file from file system into json object
# with open('config.json') as f:
#     config = json.load(f)


# Check config.json has updated credentials
# if config['ssid'] == '':
#     assert False, 'config.json ssid value is empty'


def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wifi ...')
        wlan.connect('Chaz&Annie', 'Watermelon23')
        # request = urequests.get('https://telexi.seawolfsoftware.io/api/v1/')
        # print(request)
        while not wlan.isconnected():
            pass
    print('Network Configuration:', wlan.ifconfig())


def connect_to_socket():


    url = 'https://telexi.seawolfsoftware.io/api/v1/'
    _, _, host, path = url.split('/', 3)


    while True:
        s = socket.socket()
        addr = socket.getaddrinfo('157.230.93.255', 80)[0][-1]
        s.connect(addr)

        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))

        data = s.recv(100)

        time.sleep(3)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
        s.close()


connect_to_wifi()
connect_to_socket()
