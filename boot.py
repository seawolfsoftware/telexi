import json
import network
import os
import socket
import time
import urequests
import machine


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
        print(addr)
        s.connect(addr)

        # method = (bytes('GET /api/v1/', 'utf-8'))
        # path = (bytes('api/v1/\n', 'utf-8'))
        # protocol = (bytes('HTTP/1.1\n', 'utf-8'))
        # encoding = (bytes('Accept-Encoding: gzip, deflate\n', 'utf-8'))
        # accept = (bytes('Accept: */*\n', 'utf-8'))
        # accept_language = (bytes('Accept-Language: en-us\n', 'utf-8'))
        # host = (bytes('Host: telexi.seawolfsoftware.io\n\n', 'utf-8'))

        request = bytes("GET /api/v1/ HTTP/1.1\r\nHost: telexi.seawolfsoftware.io\r\n\r\n", 'utf-8')
        # request = b"".join([method])
        s.send(request)

        data = s.recv(1024)
        time.sleep(1)

        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
        s.close()


def post_to_upstream_socket():

    url = config['server_url']
    _, _, host, path = url.split('/', 3)

    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = socket.getaddrinfo(config['server_ip'], 80)[0][-1]
        print(addr)
        s.connect(addr)

        body_dict = '{"device_id":"gdd", "is_button_on": "true"}\r\n'
        raw_content_length = 'Content-Length: ' + str(len(body_dict)) + '\r\n\r\n'
        method = bytes('POST /', 'utf-8')
        path = bytes('api/v1/ ', 'utf-8')
        protocol = bytes('HTTP/1.1\r\n', 'utf-8')
        host = bytes("Host: telexi.seawolfsoftware.io\r\n", 'utf-8')
        content_type = bytes('Content-Type: application/json\r\n', 'utf-8')
        content_length = bytes(raw_content_length, 'utf-8')

        # body_dict = '{"device_id": "aye", "is_button_on": "true"}\r\n'
        # dumped_json_string = json.dumps(body_dict)

        # convert json string to binary
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


connect_to_wifi()

tp = machine.TouchPad(machine.Pin(14))

while True:
    print(tp.read())
    time.sleep(2)



# post_to_upstream_socket()
