
import json
import paho.mqtt.client as mqtt
from EdgeServer import Edge_Server


HOST = "localhost"
PORT = 1883
    
class AC_Device():
    
    _MIN_TEMP = 18  
    _MAX_TEMP = 32
    ac_device_list = []

    def __init__(self, device_id, room):
        
        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = "AC"
        self._switch_status = "OFF"
        self._device_list = []
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect  
        self.client.connect(HOST, PORT, keepalive=60)  
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)


    # calling registration method to register the device
    def _register_device(self, device_id, room_type, device_type):
        self._device_registration_flag = True
        message = {"device_id": device_id, "room_type": room_type, "device_type": device_type}
        self.client.publish("sh/device/registration", json.dumps(message), qos=1)
        message.update({"temperature": self._temperature,
                        "switch_status": self._switch_status, "registered": self._device_registration_flag})
        if not any(devices['device_id'] == device_id for devices in self.ac_device_list):
            self.ac_device_list.append(message)


    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        self.client.subscribe("sh/device/registration/response", qos=1)
        self.client.subscribe("sh/status/request", qos=1)
        self.client.subscribe("sh/set/#", qos=1)
        self.client.subscribe("sh/get/#", qos=1)

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg): 
        if(msg.topic == "sh/device/registration/response"):
            for device in self.ac_device_list:
                if (device["device_id"] == self._device_id):
                    device["registered"] = True
                    print(msg.payload.decode("utf-8"))
        elif (msg.topic == "sh/status/request"):
            payload = msg.payload.decode("utf-8")
            device_status_list = self._get_device_status(payload)
            self.client.publish("sh/status/response/ac", json.dumps(device_status_list), qos=1)
        elif (msg.topic == "sh/set/switch_status"):
            payload = json.loads(msg.payload)
            result = self._set_switch_status(payload)
            self.client.publish("sh/status/response/ac", json.dumps(result), qos=1)
        elif (msg.topic == "sh/get/switch_status"):
            payload = msg.payload.decode("utf-8")
            device_status_list = self._get_switch_status(payload)
            self.client.publish("sh/status/response/ac", json.dumps(device_status_list), qos=1)
        elif (msg.topic == "sh/set/temp"):
            payload = json.loads(msg.payload)
            result = self._set_temperature(payload)
            self.client.publish("sh/status/response/ac", json.dumps(result), qos=1)
        elif (msg.topic == "sh/get/temp"):
            payload = msg.payload.decode("utf-8")
            device_status_list = self._get_temperature(payload)
            self.client.publish("sh/status/response/ac", json.dumps(device_status_list), qos=1)



    # Getting the current switch status of devices 
    def _get_switch_status(self, criteria):
        status_list = []
        if (criteria in ("AC", "All")):
            for device in self.ac_device_list:
                if (device["registered"] == True):
                    temp_dict = {"Device_id": device["device_id"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        elif (criteria in Edge_Server.get_room_type()):
            for device in self.ac_device_list:
                if ((device["registered"] == True) and (device["room_type"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        elif (criteria in list((devices['device_id'] for devices in self.ac_device_list))):
            for device in self.ac_device_list:
                if ((device["registered"] == True) and (device["device_id"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        return status_list

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        successOrFailure = {"result": "SUCCESS"}
        result = []
        for key in switch_state:
            if (key in ("AC", "All")):
                for device in self.ac_device_list:
                    if (device["registered"] == True):
                        device["switch_status"] = switch_state[key]
            elif (key in Edge_Server.get_room_type()):
                for device in self.ac_device_list:
                    if ((device["registered"] == True) and (device["room_type"] == key)):
                        device["switch_status"] = switch_state[key]
            elif (key in list((devices['device_id'] for devices in self.ac_device_list))):
                for device in self.ac_device_list:
                    if ((device["registered"] == True) and (device["device_id"] == key)):
                        device["switch_status"] = switch_state[key]
            else:
                successOrFailure["result"] = "FAILURE"
                break
        result.append(successOrFailure)
        return result

    # Getting the temperature for the devices
    def _get_temperature(self, criteria):
        status_list = []
        if (criteria in ("AC", "All")):
            for device in self.ac_device_list:
                if (device["registered"] == True):
                    temp_dict = {"Device_id": device["device_id"], "Temperature": device["temperature"]}
                    status_list.append(temp_dict)
        elif (criteria in Edge_Server.get_room_type()):
            for device in self.ac_device_list:
                if ((device["registered"] == True) and (device["room_type"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Temperature": device["temperature"]}
                    status_list.append(temp_dict)
        elif (criteria in list((devices['device_id'] for devices in self.ac_device_list))):
            for device in self.ac_device_list:
                if ((device["registered"] == True) and (device["device_id"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Temperature": device["temperature"]}
                    status_list.append(temp_dict)
        return status_list

    # Setting up the temperature of the devices
    def _set_temperature(self, temperature):
        successOrFailure = {"result": "SUCCESS"}
        result = []
        for key in temperature:
            if((temperature[key] >= self._MIN_TEMP) and temperature[key] <= self._MAX_TEMP):
                if (key in ("AC", "All")):
                    for device in self.ac_device_list:
                        if (device["registered"] == True):
                            device["temperature"] = temperature[key]
                elif (key in Edge_Server.get_room_type()):
                    for device in self.ac_device_list:
                        if ((device["registered"] == True) and (device["room_type"] == key)):
                            device["temperature"] = temperature[key]
                elif (key in list((devices['device_id'] for devices in self.ac_device_list))):
                    for device in self.ac_device_list:
                        if ((device["registered"] == True) and (device["device_id"] == key)):
                            device["temperature"] = temperature[key]
                else:
                    successOrFailure["result"] = "FAILURE"
                    break
            else:
                successOrFailure["result"] = "FAILURE"
                break
        result.append(successOrFailure)
        return result

    # Getting the status of devices
    def _get_device_status(self, criteria):
        status_list = []
        if (criteria in ("AC", "All")):
            for device in self.ac_device_list:
                if (device["registered"] == True):
                    temp_dict = {"Device_id": device["device_id"], "Room": device["room_type"],
                                 "Temperature": device["temperature"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        elif (criteria in Edge_Server.get_room_type()):
            for device in self.ac_device_list:
                if ((device["registered"] == True) and (device["room_type"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Room": device["room_type"],
                                 "Temperature": device["temperature"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        elif (criteria in list((devices['device_id'] for devices in self.ac_device_list))):
            for device in self.ac_device_list:
                if ((device["registered"] == True) and (device["device_id"] == criteria)):
                    temp_dict = {"Device_id": device["device_id"], "Room": device["room_type"],
                                 "Temperature": device["temperature"], "Switch": device["switch_status"]}
                    status_list.append(temp_dict)
        return status_list
    
    def _on_disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()