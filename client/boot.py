import json
import network
import socket
import time
from Interact import *
from machine import Pin, TouchPad
import esp32

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

        # returns a list of addresses, 
        # and each address has more information than we need. 
        # We want to get just the first valid address, 
        # and then just the IP address and port of the server
        addr = socket.getaddrinfo(config['server_ip'], 80)[0][-1]
        print('Socket address is:', addr)

        # Connect to upstream socket
        s.connect(addr)


def listen_for_touch_events():

        # pin_14 = Interact(TouchPad(Pin(14)),
        #                     touch_sensitivity=250,
        #                     callback=lambda event, clicks: print(event, clicks))
        #
        # pin_13 = Interact(TouchPad(Pin(13)),
        #                   touch_sensitivity=250,
        #                   callback=lambda event, clicks: print(event, clicks))

        pin_12 = Interact(TouchPad(Pin(12)),
                          touch_sensitivity=250,
                          callback=lambda event, clicks: print(event, clicks))

        led = Pin(2, Pin.OUT)


        # Listen for touch events every 10ms
        while True:
            pin_12.update()

            if pin_12.value() == 1:
                led.on()
                print('Outside')
                post_event_to_api()
                led.off()

            continue


def post_event_to_api():

    url = config['server_url']
    _, _, host, path = url.split('/', 3)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = socket.getaddrinfo(config['server_ip'], 8000)[0][-1]
    print('Socket address is:', addr)

    # Connect to upstream socket
    s.connect(addr)

    method = bytes('POST /', 'utf-8')
    path = bytes('api/v1/press_events/ ', 'utf-8')
    protocol = bytes('HTTP/1.1\r\n', 'utf-8')
    host = bytes("Host: 10.0.0.147\r\n", 'utf-8')
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

    s.close()


connect_to_wifi()
# start_local()
# connect_to_upstream_socket()
listen_for_touch_events()
