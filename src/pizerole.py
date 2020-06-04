import ble_devices, actions
from datetime import datetime
from bluepy.btle import Scanner, DefaultDelegate
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            for device in ble_devices.get_devices():
                if device.get('mac') == dev.addr:
                    print("DETECTED: button: %s, Name: %s" % (device.get('mac'), device.get('name')))
                    if device.get('name') == "coffee":
                        actions.notify(device)
                    elif device.get('name') == "towel":
                        actions.broadcast(device)
                    elif device.get('name') == "livingroom":
                        if device.get('state') == actions.OFF_STATE:
                            if device.get('previous_state') == actions.OFF_STATE:
                                device['state'] = actions.BRIGHTEN_STATE
                            if device.get('previous_state') == actions.DARKEN_STATE:
                                device['state'] = actions.BRIGHTEN_STATE
                            if device.get('previous_state') == actions.BRIGHTEN_STATE:
                                device['state'] = actions.DARKEN_STATE
                    else:
                        actions.toggle(device)

scanner = Scanner().withDelegate(ScanDelegate())
while True:
    devices = scanner.scan(1.0)
    if ble_devices.AIRER.get("state") == 1:
    # lets see if its been on for 8 hours and if so turn it off
        lastUpdated = ble_devices.AIRER.get("lastUpdated", datetime)
        timeSinceTurnedOn = datetime.now() - lastUpdated
        if timeSinceTurnedOn.seconds >= (8*(60*60)):
        # turn off
            print("Timer has been on for %d hours and %d minutes" % ((timeSinceTurnedOn.seconds/60/60), ((timeSinceTurnedOn.seconds)/60) % 60))
            actions.toggle(ble_devices.AIRER)
    if ble_devices.LIVING_ROOM_LIGHTS.get("state") > 0:
        print("lights triggered")
        actions.changeLights(ble_devices.LIVING_ROOM_LIGHTS)


