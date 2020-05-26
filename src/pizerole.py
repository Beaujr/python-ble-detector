from bluepy.btle import Scanner, DefaultDelegate
import http.client
from datetime import datetime

# https://github.com/greghesp/assistant-relay
RELAY_ASSISTANT = "nuc.beau.cf:3001"
RELAY_USER = "beau"
DESK = {'mac': 'AB:CD:EF:GH:IJ:KL', 'name': 'Desk', 'state': 0, 'lastUpdated': datetime.now()}
BLE_STATES = [DESK]

def toggle(device):
    conn = http.client.HTTPConnection(RELAY_ASSISTANT)
    lastUpdated = device.get("lastUpdated", datetime)
    name = device.get('name')
    lastToggled = datetime.now() - lastUpdated
    if lastToggled.seconds > 10:
        state = "off"
        if device.get("state") == 0:
            state = "on"
        payload = "{\"user\":\"%s\",\"command\":\"turn %s %s\", \"broadcast\": false}" % (RELAY_ASSISTANT, name, state)
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

        conn.request("POST", "/assistant", payload, headers)

        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        device["lastUpdated"] = datetime.now()
        if state == "on":
            device["state"] = 1
        elif state == "off":
            device["state"] = 0
        print(device["lastUpdated"])
        print("Device %s toggled to %s" % (name, state))
    else:
        print("%s last toggled %d seconds ago" % (name, lastToggled.seconds))


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            for button in BLE_STATES:
                if button.get('mac') == dev.addr:
                    print("DETECTED: button: %s, Name: %s" % (button.get('mac'), button.get('name')))
                    toggle(button)
scanner = Scanner().withDelegate(ScanDelegate())
while True:
    devices = scanner.scan(1.0)


