import machine
from network import WLAN

# boot.py -- run on boot-up
SSID = 'MOVISTAR_6C62'
AUTH = 'C066CF732354AEE45C16'

wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    print(nets)
    if net.ssid == SSID:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, AUTH), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!',wlan.ifconfig())
        break
