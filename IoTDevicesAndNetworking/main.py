import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 1.0

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user

edge_server_1 = Edge_Server('edge_server_1')
time.sleep(WAIT_TIME)



# Creating the light_device
print("Intitate the device creation and registration process." )
print("\nCreating the Light devices for their respective rooms.")
# light_device_1 = Light_Device("light_1", "Kitchen")

light1 = Light_Device('l_001', 'BR1')
time.sleep(WAIT_TIME)
light2 = Light_Device('l_002', 'BR2')
time.sleep(WAIT_TIME)
light3 = Light_Device('l_003', 'Kitchen')
time.sleep(WAIT_TIME)
ac1 = AC_Device('ac_001', 'BR1')
time.sleep(WAIT_TIME)
ac2 = AC_Device('ac_002', 'BR2')
time.sleep(WAIT_TIME)
#
print("\nList of registered devices:")
registered_device_list = edge_server_1.get_registered_device_list()
print(registered_device_list)
# # Creating the ac_device
# print("\nCreating the AC devices for their respective rooms. ")
# ac_device_1 = AC_Device("ac_1", "BR1")
time.sleep(WAIT_TIME)


all_device_status_list = edge_server_1.get_status("ALL".title())
print("\n\nStatus of all devices:\n", all_device_status_list)
time.sleep(WAIT_TIME)

all_light_devices_status = edge_server_1.get_status("LIGHT")
print("\n\nStatus of all light devices:\n", all_light_devices_status)
time.sleep(WAIT_TIME)

all_ac_devices_status = edge_server_1.get_status("AC")
print("\n\nStatus of all ac devices:\n", all_ac_devices_status)
time.sleep(WAIT_TIME)

room = "BR1"
room_devices_status = edge_server_1.get_status(room)
print(f"\n\nStatus of all devices in {room}:\n", room_devices_status)
time.sleep(WAIT_TIME)

device_id = "l_003"
device_id_status = edge_server_1.get_status(device_id)
print(f"\n\nStatus of the device {device_id}:\n", device_id_status)
time.sleep(WAIT_TIME)

device_id = "l_002"
switch_status = "ON"
device_id_status = edge_server_1.set({"device_id": device_id, "switch_status":switch_status})
print(f"\n\nSwitch Status of the device {device_id}:\n", device_id_status)
time.sleep(WAIT_TIME)

all_device_status_list = edge_server_1.get_status("ALL".title())
print("\n\nStatus of all devices:\n", all_device_status_list)
time.sleep(WAIT_TIME)


room = "BR1"
switch_status = "ON"
room_devices_status = edge_server_1.set({"room_type": room, "switch_status":switch_status})
print(f"\n\nSwitch Status of all devices in {room}:\n", room_devices_status)
time.sleep(WAIT_TIME)

all_device_status_list = edge_server_1.get_status("ALL".title())
print("\n\nStatus of all devices:\n", all_device_status_list)
time.sleep(WAIT_TIME)


device_type = "AC"
switch_status = "ON"
all_ac_devices_status = edge_server_1.set({"device_type": device_type, "switch_status":switch_status})
print("\n\nSwitch Status of all ac devices:\n", all_ac_devices_status)
time.sleep(WAIT_TIME)

all_device_status_list = edge_server_1.get_status("ALL".title())
print("\n\nStatus of all devices:\n", all_device_status_list)
time.sleep(WAIT_TIME)

device = "ALL"
switch_status = "ON"
all_devices_status = edge_server_1.set({"device_type": device.title(), "switch_status":switch_status})
print("\n\nSwitch Status of all devices:\n", all_devices_status)
time.sleep(WAIT_TIME)

all_device_status_list = edge_server_1.get_status("ALL".title())
print("\n\nStatus of all devices:\n", all_device_status_list)
time.sleep(WAIT_TIME)


device_id = "l_002"
intensity = "High"
device_id_status = edge_server_1.set({"device_id": device_id, "intensity":intensity})
print(f"\n\nIntensity of the device {device_id}:\n", device_id_status)
time.sleep(WAIT_TIME)

all_device_status_list = edge_server_1.get_status("ALL".title())
print("\n\nStatus of all devices:\n", all_device_status_list)
time.sleep(WAIT_TIME)

room = "BR1"
intensity = "Medium"
room_devices_status = edge_server_1.set({"room_type": room, "intensity":intensity})
print(f"\n\nIntensity of all devices in {room}:\n", room_devices_status)
time.sleep(WAIT_TIME)

all_device_status_list = edge_server_1.get_status("ALL".title())
print("\n\nStatus of all devices:\n", all_device_status_list)
time.sleep(WAIT_TIME)

device = "ALL"
intensity = "Low"
all_devices_status = edge_server_1.set({"device_type": device.title(), "intensity": intensity})
print("\n\nIntensity of all light devices:\n", all_devices_status)
time.sleep(WAIT_TIME)

all_device_status_list = edge_server_1.get_status("ALL".title())
print("\n\nStatus of all devices:\n", all_device_status_list)
time.sleep(WAIT_TIME)

device_id = "ac_002"
temperature = 35
device_id_status = edge_server_1.set({"device_id": device_id, "temperature": temperature})
print(f"\n\nTemperature of the device {device_id}:\n", device_id_status)
time.sleep(WAIT_TIME)

all_device_status_list = edge_server_1.get_status("ALL".title())
print("\n\nStatus of all devices:\n", all_device_status_list)
time.sleep(WAIT_TIME)

room = "BR1"
temperature = 25
room_devices_status = edge_server_1.set({"room_type": room, "temperature": temperature})
print(f"\n\nTemperature of all devices in {room}:\n", room_devices_status)
time.sleep(WAIT_TIME)

all_device_status_list = edge_server_1.get_status("ALL".title())
print("\n\nStatus of all devices:\n", all_device_status_list)
time.sleep(WAIT_TIME)

device = "ALL"
temperature = 30
all_devices_status = edge_server_1.set({"device_type": device.title(), "temperature": temperature})
print("\n\nTemperature of all ac devices:\n", all_devices_status)
time.sleep(WAIT_TIME)

all_device_status_list = edge_server_1.get_status("ALL".title())
print("\n\nStatus of all devices:\n", all_device_status_list)
time.sleep(WAIT_TIME)

print("\nSmart Home Simulation stopped.")
edge_server_1.terminate()
