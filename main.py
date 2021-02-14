
print('Running: main.py')

import sys
from time import sleep
from MicroWebSrv2.MicroWebSrv2 import WebRoute, GET
from MicroWebSrv2.MicroWebSrv2.libs.XAsyncSockets import XAsyncSocketsPool
from MicroWebSrv2.MicroWebSrv2.microWebSrv2 import MicroWebSrv2

xasPool = XAsyncSocketsPool()
srvHttp = MicroWebSrv2()
# srvHttp.BindAddress = ('192.168.0.1', 12345)

# TODO make switch to SSL
# srvHttps = MicroWebSrv2()
# /Users/chaz/miniconda3/ssl
# srvHttps.EnableSSL(certFile='cert/host.cert',
#                    keyFile='cert/host.key')
# srvHttps.StartInPool(xasPool)

srvHttp.StartInPool(xasPool)

xasPool.AsyncWaitEvents(threadsCount=1)


@WebRoute(GET, '/local')
def RequestTest(microWebSrv2, request):
    request.Response.ReturnOkJSON({
        'Method': request.Method,
        'Authorization': request.Authorization,
        'isSSL': request.IsSSL,
        'Client Address': request.UserAddress,
        'Host': request.Host,
        'Origin': request.Origin,
        'Path': request.Path,
        'Accept': request.Accept,
        'UserAgent': request.UserAgent,
        'HttpVer': request.HttpVer,
        'QueryString': request.QueryString,
        'QueryParams': request.QueryParams,

    })


try:
    while True:
        sleep(1)

except KeyboardInterrupt:
    srvHttp.Stop()
    # srvHttps.Stop()
    xasPool.StopWaitEvents()



########
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