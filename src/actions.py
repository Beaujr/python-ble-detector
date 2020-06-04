import http.client, ssl
from datetime import datetime

OFF_STATE = 0
BRIGHTEN_STATE = 1
DARKEN_STATE = 2

# https://github.com/greghesp/assistant-relay
RELAY_ASSISTANT = "nuc.beau.cf"
RELAY_USER = "beau"
fcm_conn = http.client.HTTPSConnection(RELAY_ASSISTANT)


def changeLights(light):
    current_state = light.get("state")
    if current_state == OFF_STATE:
        return
    current_brightness = light.get("current")
    light_last_changed = light.get("lastUpdated", datetime)
    last_toggled = datetime.now() - light_last_changed

    buffer_seconds = 1
    if last_toggled.seconds < buffer_seconds:
        return
    dimmer_length_mins = 20
    dimmer_length_secs = 60 * dimmer_length_mins

    brightness_step = 100 / (dimmer_length_secs / buffer_seconds)
    print("STATE: %d BRIGHTNESS: %d" % (current_state, current_brightness))

    if current_state == DARKEN_STATE and current_brightness != 0:
        int_brightness = int(round(current_brightness - brightness_step))
        print(int_brightness)
        if int_brightness < 0:
            int_brightness = 0
        if int_brightness == current_brightness:
            int_brightness = int_brightness - 1
        update_light(light, int_brightness)
    elif current_state == BRIGHTEN_STATE and current_brightness != 100:
        int_brightness = int(round(current_brightness + brightness_step))
        if int_brightness > 100:
            int_brightness = 100
        update_light(light, int_brightness)

    if (current_brightness <= 0 and current_state == DARKEN_STATE) or (
            current_brightness >= 100 and current_state == BRIGHTEN_STATE):
        light["state"] = OFF_STATE
        light["previous_state"] = DARKEN_STATE if (0 == current_brightness) else BRIGHTEN_STATE


def update_light(light, brightness):
    if brightness != light["current"]:
        light["current"] = brightness
        print("dimming %s" % light["current"])
        payload = "{\"user\":\"%s\",\"command\":\"turn %s lights to %d percent\"}" % (
            RELAY_USER, light.get('name'), light["current"])
        call_google_assistant(payload)
    light["lastUpdated"] = datetime.now()


def toggle(device):
    lastUpdated = device.get("lastUpdated", datetime)
    name = device.get('name')
    lastToggled = datetime.now() - lastUpdated
    if lastToggled.seconds > 10:
        state = "off"
        if device.get("state") == 0:
            state = "on"
        payload = "{\"user\":\"%s\",\"command\":\"turn %s %s\"}" % (RELAY_USER, name, state)
        call_google_assistant(payload)

        device["lastUpdated"] = datetime.now()
        if state == "on":
            device["state"] = 1
        elif state == "off":
            device["state"] = 0
        print(device["lastUpdated"])
        print("Device %s toggled to %s" % (name, state))
        send_message("Button", "Device %s toggled to %s" % (name, state))
    else:
        print("%s last toggled %d seconds ago" % (name, lastToggled.seconds))


def call_google_assistant(payload):
    assistant_conn = http.client.HTTPSConnection(RELAY_ASSISTANT, timeout=5, context=ssl._create_unverified_context())
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "2c4ddc5b-513c-e018-3055-95587ed51ee0"
    }
    assistant_conn.request("POST", "/assistant", payload, headers)
    res = assistant_conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


def call_fcm(payload, topic):
    fcm_conn = http.client.HTTPSConnection("nuc.beau.cf")
    headers = {
        'content-type': "application/json"
    }
    fcm_conn.request("POST", "/fcm/send/%s" % topic, payload, headers)
    res = fcm_conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


def broadcast(device):
    lastUpdated = device.get("lastUpdated", datetime)
    name = device.get('name')
    lastToggled = datetime.now() - lastUpdated
    print("%s last toggled %d seconds ago" % (name, lastToggled.seconds))
    if lastToggled.seconds > 30:
        payload = "{\"user\":\"%s\",\"command\":\"%s\", \"broadcast\": true}" % (RELAY_USER, device.get('message'))
        call_google_assistant(payload)
        device["lastUpdated"] = datetime.now()


def notify(device):
    send_message(device.get('title'), device.get('message'))


def send_message(title, message):
    payload = "{ \"title\": \"%s\", \"body\":\"%s\", \"image\": \"\"}" % (title, message)
    call_fcm(payload, "devices")

