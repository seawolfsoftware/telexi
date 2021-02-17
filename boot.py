import json
import network
import os
import socket
import time
import urequests


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
        # request = urequests.get('https://telexi.seawolfsoftware.io/api/v1/')
        # print(request)
        while not wlan.isconnected():
            pass
    print('Network Configuration:', wlan.ifconfig())


def connect_to_socket():

    url = config['server_url']
    _, _, host, path = url.split('/', 3)

    while True:
        s = socket.socket()
        addr = socket.getaddrinfo(config['server_ip'], 80)[0][-1]
        s.connect(addr)

        s.send(b"GET /%s HTTP/1.1\r\n Host: %s\r\n" % (bytes(path, "utf-8"), bytes(host, "utf-8")))

        # s.send(bytes('GET %s '
        #              'HTTP/1.1\r\n'
        #              'Host: %s\r\n\r\n' %
        #              ('api/v1/', 'telexi.seawolfsoftware.io'), 'utf-8'))

        # s.send(bytes('GET /api/v1/ HTTP/1.1\r\nHost: telexi.seawolfsoftware.io\r\n\r\n'), 'utf-8')
        # GET / HTTP / 1.1\r\nHost: www.google.com\r\n\r\n

        data = s.recv(1024)
        time.sleep(1)

        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
        s.close()


connect_to_wifi()
connect_to_socket()
