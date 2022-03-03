import json
import paho.mqtt.client as mqtt
from EdgeServer import Edge_Server

HOST = "localhost"
PORT = 1883


class Light_Device():

    light_device_list = []

    # setting up the intensity choices for Smart Light Bulb
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]



    def __init__(self, device_id, room):
        # Assigning device level information for each of the devices. 
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = "LIGHT"
        self._switch_status = "OFF"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect
        self.client.connect(HOST, PORT, keepalive=60)  
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)





    def _register_device(self, device_id, room_type, device_type):
        self._device_registration_flag = True
        message = {"device_id": device_id, "room_type": room_type, "device_type": device_type}
        self.client.publish("sh/device/registration", json.dumps(message), qos=1)
        message.update({"intensity": self._light_intensity, "switch_status": self._switch_status,
                        "registered": self._device_registration_flag})
        if not any(devices['device_id'] == device_id for devices in self.light_device_list):
            self.light_device_list.append(message)


    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        self.subscribe_status = self.client.subscribe("sh/device/registration/response", qos=1)
        self.client.subscribe("sh/status/request", qos=1)
        self.client.subscribe("sh/set/#", qos=1)
        self.client.subscribe("sh/get/#", qos=1)

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        if(msg.topic == "sh/device/registration/response"):
            for device in self.light_device_list:
                if (device["device_id"] == self._device_id):
                    device["registered"] = True
                    print(str(msg.payload.decode("utf-8")))
        elif(msg.topic == "sh/status/request"):
            payload = msg.payload.decode("utf-8")
            device_status_list = self._get_device_status(payload)
            self.client.publish("sh/status/response/light", json.dumps(device_status_list), qos=1)
        elif(msg.topic == "sh/set/switch_status"):
            payload = json.loads(msg.payload)
            device_status_list = self._set_switch_status(payload)
            self.client.publish("sh/status/response/light", json.dumps(device_status_list), qos=1)
        elif (msg.topic == "sh/get/switch_status"):
            payload = msg.payload.decode("utf-8")
            device_status_list = self._get_switch_status(payload)
            self.client.publish("sh/status/response/light", json.dumps(device_status_list), qos=1)
        elif (msg.topic == "sh/set/intensity"):
            payload = json.loads(msg.payload)
            device_status_list = self._set_light_intensity(payload)
            self.client.publish("sh/status/response/light", json.dumps(device_status_list), qos=1)
        elif (msg.topic == "sh/get/intensity"):
            payload = msg.payload.decode("utf-8")
            device_status_list = self._get_light_intensity(payload)
            self.client.publish("sh/status/response/light", json.dumps(device_status_list), qos=1)





    # Getting the current switch status of devices 
    def _get_switch_status(self, criteria):
        status_list = []
        if (criteria in ("LIGHT", "All")):
            for device in self.light_device_list:
                if (device["registered"] == True):
                    temp_dict = {"Device_id": device["device_id"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        elif (criteria in Edge_Server.get_room_type()):
            for device in self.light_device_list:
                if ((device["registered"] == True) and (device["room_type"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        elif (criteria in list((devices['device_id'] for devices in self.light_device_list))):
            for device in self.light_device_list:
                if ((device["registered"] == True) and (device["device_id"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        return status_list

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        successOrFailure = {"result": "SUCCESS"}
        result = []
        for key in switch_state:
            if (key in ("LIGHT", "All")):
                for device in self.light_device_list:
                    if (device["registered"] == True):
                        device["switch_status"] = switch_state[key]
            elif (key in Edge_Server.get_room_type()):
                for device in self.light_device_list:
                    if ((device["registered"] == True) and (device["room_type"] == key)):
                        device["switch_status"] = switch_state[key]
            elif (key in list((devices['device_id'] for devices in self.light_device_list))):
                for device in self.light_device_list:
                    if ((device["registered"] == True) and (device["device_id"] == key)):
                        device["switch_status"] = switch_state[key]
            else:
                successOrFailure["result"] = "FAILURE"
                break
        result.append(successOrFailure)
        return result

    # Getting the light intensity for the devices
    def _get_light_intensity(self, criteria):
        status_list = []
        if (criteria in ("LIGHT", "All")):
            for device in self.light_device_list:
                if (device["registered"] == True):
                    temp_dict = {"Device_id": device["device_id"], "Intensity": device["intensity"]}
                    status_list.append(temp_dict)
        elif (criteria in Edge_Server.get_room_type()):
            for device in self.light_device_list:
                if ((device["registered"] == True) and (device["room_type"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Intensity": device["intensity"]}
                    status_list.append(temp_dict)
        elif (criteria in list((devices['device_id'] for devices in self.light_device_list))):
            for device in self.light_device_list:
                if ((device["registered"] == True) and (device["device_id"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Intensity": device["intensity"]}
                    status_list.append(temp_dict)
        return status_list

    # Setting the light intensity for devices
    def _set_light_intensity(self, light_intensity):
        successOrFailure = {"result": "SUCCESS"}
        result = []
        for key in light_intensity:
            if (key in ("LIGHT", "All")):
                for device in self.light_device_list:
                    if (device["registered"] == True):
                        device["intensity"] = light_intensity[key].upper()
            elif (key in Edge_Server.get_room_type()):
                for device in self.light_device_list:
                    if ((device["registered"] == True) and (device["room_type"] == key)):
                        device["intensity"] = light_intensity[key].upper()
            elif (key in list((devices['device_id'] for devices in self.light_device_list))):
                for device in self.light_device_list:
                    if ((device["registered"] == True) and (device["device_id"] == key)):
                        device["intensity"] = light_intensity[key].upper()
            else:
                successOrFailure["result"] = "FAILURE"
                break
        result.append(successOrFailure)
        return result

    # Getting the status of devices
    def _get_device_status(self, criteria):
        status_list = []
        if (criteria in ("LIGHT", "All")):
            for device in self.light_device_list:
                if (device["registered"] == True):
                    temp_dict = {"Device_id": device["device_id"], "Room": device["room_type"],
                                 "Intensity": device["intensity"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        elif (criteria in Edge_Server.get_room_type()):
            for device in self.light_device_list:
                if ((device["registered"] == True) and (device["room_type"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Room": device["room_type"],
                                 "Intensity": device["intensity"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        elif (criteria in list((devices['device_id'] for devices in self.light_device_list))):
            for device in self.light_device_list:
                if ((device["registered"] == True) and (device["device_id"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Room": device["room_type"],
                                 "Intensity": device["intensity"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        return status_list

    def _on_disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()





