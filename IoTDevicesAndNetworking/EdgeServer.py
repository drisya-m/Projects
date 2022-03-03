
import json
import time
import paho.mqtt.client as mqtt


HOST = "localhost"
PORT = 1883     
WAIT_TIME = 0.25

class Edge_Server:

    # setting up the room types
    _ROOM_TYPE = ["BR1", "BR2", "Kitchen"]
    device_status_list = []

    @classmethod
    def get_room_type(cls):
        return cls._ROOM_TYPE
    
    def __init__(self, instance_name):
        
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._registered_list = []

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        if(result_code == 0):
            print("Broker connection ok")
        else:
            print("Broker not connected")
        self.client.subscribe("sh/device/registration", qos=1)
        self.client.subscribe("sh/status/response/#", qos=1)

        
    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        if(msg.topic == "sh/device/registration"):
            payload = json.loads(msg.payload)
            if not any(devices['device_id'] == payload["device_id"] for devices in self._registered_list):
                self._registered_list.append(payload)
                response = "Device " + payload['device_id'] + " registered successfully"
                self.client.publish("sh/device/registration/response", response, qos=2)
        elif(msg.topic in ["sh/status/response/light", "sh/status/response/ac"]):
            payload = json.loads(msg.payload)
            for devices in payload:
                if('Device_id' in devices.keys()):
                    if not any(device1['Device_id'] == devices["Device_id"] for device1 in self.device_status_list):
                        self.device_status_list.append(devices)
                elif('result' in devices.keys()):
                    self.device_status_list.append(devices)




    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list

    # Getting the status for the connected devices
    def get_status(self, status_criteria):
        self.device_status_list.clear()
        self.client.publish("sh/status/request", status_criteria, qos=1)
        time.sleep(WAIT_TIME)
        return self.device_status_list


    # Controlling and performing the operations on the devices
    # based on the request received
    def set(self, set_criteria):
        self.device_status_list.clear()
        key = set_criteria.keys()
        if("switch_status" in key):
            value = iter(list(set_criteria.values()))
            message = dict(zip(value, value))
            self.client.publish("sh/set/switch_status", json.dumps(message), qos=1)
            time.sleep(WAIT_TIME)
            for rec in self.device_status_list:
                if(("result" in rec.keys()) and (rec["result"] == "SUCCESS")):
                    self.device_status_list.clear()
                    self.client.publish("sh/get/switch_status", str(list(message.keys())[0]), qos=1)
                    time.sleep(WAIT_TIME)
                elif (("result" in rec.keys()) and (rec["result"] == "FAILURE")):
                    self.device_status_list = [{"Result": "Parameters incorrect"}]
        elif("intensity" in key):
            value = iter(list(set_criteria.values()))
            message = dict(zip(value, value))
            self.client.publish("sh/set/intensity", json.dumps(message), qos=1)
            time.sleep(WAIT_TIME)
            for rec in self.device_status_list:
                if(("result" in rec.keys()) and (rec["result"] == "SUCCESS")):
                    self.device_status_list.clear()
                    self.client.publish("sh/get/intensity", str(list(message.keys())[0]), qos=1)
                    time.sleep(WAIT_TIME)
                elif(("result" in rec.keys()) and (rec["result"] == "FAILURE")):
                    self.device_status_list = [{"Result": "Parameters incorret"}]
        elif ("temperature" in key):
            value = iter(list(set_criteria.values()))
            message = dict(zip(value, value))
            self.client.publish("sh/set/temp", json.dumps(message), qos=1)
            time.sleep(WAIT_TIME)
            for rec in self.device_status_list:
                if(("result" in rec.keys()) and (rec["result"] == "SUCCESS")):
                    self.device_status_list.clear()
                    self.client.publish("sh/get/temp", str(list(message.keys())[0]), qos=1)
                    time.sleep(WAIT_TIME)
                elif(("result" in rec.keys()) and (rec["result"] == "FAILURE")):
                    self.device_status_list = [{"Result": "Temperature out of range"}]
        return self.device_status_list
