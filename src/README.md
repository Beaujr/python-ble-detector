# python-ble-detector

python-ble-detector is an example Docker / Python Project to detect BLE (Bluetooth Low Energy) beacons using a Raspberry Pi Zero W 

I personally use this python script to manage smart powersockets via bluetooth button detection and [assistant relay](https://github.com/greghesp/assistant-relay).

## Installation
Have docker installed on your Raspberry Pi Zero W
```makefile
make python-ble-detector 
```

## Usage
Add you own bluetooth device to the BLE_STATES array

```python
DESK = {'mac': 'AB:CD:EF:GH:IJ:KL', 'name': 'Desk', 'state': 0, 'lastUpdated': datetime.now()}
BLE_STATES = [DESK]
```

and then overwrite any custom functions you want to call in the ble [scanner function](
https://github.com/Beaujr/python-ble-detector/blob/f86694f16886b384e55a202ba2a16d6694dcd26c/src/pizerole.py#L50)
```python
def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            for button in BLE_STATES:
                if button.get('mac') == dev.addr:
                    print("DETECTED: button: %s, Name: %s" % (button.get('mac'), button.get('name')))
                    toggle(button)
```
## Contributing
Do whatever you want

## License
[MIT](https://choosealicense.com/licenses/mit/)
