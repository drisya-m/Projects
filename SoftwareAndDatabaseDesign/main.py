from model import UserModel, DeviceModel, WeatherDataModel, DailyReportModel
from datetime import datetime

# The below code demonstrates successful and unsuccessful read on user collection
# based on role of the user. If user in the "username" has role admin , proceed with search of the record
# with user_id in "key" field (admin can access all user collection documents).
# If the user in the "username" is not of role admin , return permission denied

# input for demonstration of successful read on user collection:
#username = "admin"

# input for demonstration of unsuccessful read on user collection
username = "user_2"

user_coll = UserModel()

print('Read Operation:')
access = user_coll.validate_permission(username)
if (access == -1):
    print(user_coll.latest_error)
else:
    key = 'user_2'
    user_document = user_coll.find_by_username(key)
    if (user_document == -1):
        print(user_coll.latest_error)
    else:
        print(user_document)

# The below code demonstrates successful and unsuccessful insert of single document on user collection
# based on role of the "username". If user in the "username" has role admin , proceed with insertion of the record
# for user_id passed in insert function. If the user in the "username" is not admin , return permission denied

# input for demonstration of successful read on user collection:
#username = "admin"

# input for demonstration of unsuccessful read on user collection
username = "user_2"

print('Insert operation:')
access = user_coll.validate_permission(username)
if (access == -1):
    print(user_coll.latest_error)
else:
    user_document = user_coll.insert('user_5', 'user_5@example.com', 'default', [{'DH002': 'r'}, {'DT005': 'rw'}])
    if (user_document == -1):
        print(user_coll.latest_error)
    else:
        print(user_document)

# The below code demonstrates update of a single user document
# Successful update - if "username" is having admin role
# Unsuccessful update - if "username" is having default role
# "key field will take the user_id of the document in user collection that needs to be updated
# "user_data" will take the dictionary of fields in the document to be updated

# input for demonstration of successful read on user collection:
# username = "admin"

# # input for demonstration of unsuccessful read on user collection
username = "user_2"

print('Update operation:')
access = user_coll.validate_permission(username)
if (access == -1):
    print(user_coll.latest_error)
else:
    key = "user_2"
    user_data = {'alist': [{'DT100': 'rw'}]}
    user_document = user_coll.update(key, user_data)
    if (user_document == -1):
        print(user_coll.latest_error)
    else:
        print(user_document)

# The below code demonstrates deletion of a single user document
# Successful deletion - if "username" is having admin role
# Unsuccessful deletion - if "username" is having default role
# "key field will take the user_id of the document in user collection that needs to be deleted

# input for demonstration of successful read on user collection:
#username = "admin"

# input for demonstration of unsuccessful read on user collection
username = "user_2"

print('Delete operation:')
access = user_coll.validate_permission(username)
if (access == -1):
    print(user_coll.latest_error)
else:
    key = "user_4"
    user_document = user_coll.delete(key)
    if (user_document == -1):
        print(user_coll.latest_error)
    else:
        print('{0} documents deleted'.format(user_document))



# Access validation and operations on Device Collection


device_coll = DeviceModel()


# The below code demonstrates successful and unsuccessful read on device collection
# based on device access as per alist field of the user. If user in the "username" has 'r' or 'rw' access for the
# "device_id", proceed with search of the record in the device collection else return permission denied

# Input for successful read on deivce data
# username = "user_1"
# deviceid = "DT004"

# Input for unsuccessful read on deivce data
username = "user_2"
deviceid = "DH005"


device_access = device_coll.validate_permission(username, deviceid)
if (device_access == -1):
    print(device_coll.latest_error)
else:
    print('Read device data:')
    if (device_access in ('r', 'rw')):
        device_document = device_coll.find_by_device_id(deviceid)
        if (device_document == -1):
            print(device_coll.latest_error)
        else:
            print(device_document)
    else:
        print(f'{username} does not have permission to access data for {deviceid}')


# The below code demonstrates successful and unsuccessful insert on device collection
# based on device access as per alist field of the user. If user in the "username" has 'w' or 'rw' access for the
# "device_id", proceed with insertion of the record in the device collection else return permission denied

# Input for successful insertion of deivce data
# username = "user_2"
# deviceid = "DT100"

# #Input for unsuccessful insertion of deivce data
username = "user_2"
deviceid = "DH005"

print('Insert device data:')
device_access = device_coll.validate_permission(username, deviceid)
if (device_access == -1):
    print(device_coll.latest_error)
else:
    if (device_access in ('w', 'rw')):
        device_desc = 'Temperature Sensor'
        device_type = 'Temperature'
        manufacturer = 'Acme'
        device_document = device_coll.insert(deviceid, device_desc, device_type, manufacturer)
        if (device_document == -1):
            print(device_coll.latest_error)
        else:
            print(device_document)
    else:
        print(f'{username} does not have permission to insert data for {deviceid}')


# The below code demonstrates successful and unsuccessful update on device collection
# based on device access as per alist field of the user. If user in the "username" has 'w' or 'rw' access for the
# "device_id", proceed with update of the record in the device collection else return permission denied
# user_data is the dictionary of fields to be updated

# Input for successful update of deivce data
# username = "user_2"
# deviceid = "DT100"

# #Input for unsuccessful update of deivce data
username = "user_2"
deviceid = "DH005"

print('Update device data:')
device_access = device_coll.validate_permission(username, deviceid)
if (device_access == -1):
    print(device_coll.latest_error)
else:
    if (device_access in ('w', 'rw')):
        user_data = {'manufacturer': 'Omega'}
        device_document = device_coll.update(deviceid, user_data)
        if (device_document == -1):
            print(user_coll.latest_error)
        else:
            print(device_document)
    else:
        print(f'{username} does not have permission to update data for {deviceid}')

# The below code demonstrates successful and unsuccessful delete on device collection
# based on device access as per alist field of the user. If user in the "username" has 'w' or 'rw' access for the
# "device_id", proceed with deletion of the record in the device collection else return permission denied

# Input for successful deletion of deivce data
# username = "user_2"
# deviceid = "DT100"

# #Input for unsuccessful deletion of deivce data
username = "user_2"
deviceid = "DH005"

print('Delete device data:')
device_access = device_coll.validate_permission(username, deviceid)
if (device_access == -1):
    print(device_coll.latest_error)
else:
    if (device_access in ('w', 'rw')):
        device_document = device_coll.delete(deviceid)
        if (device_document == -1):
            print(user_coll.latest_error)
        else:
            print('{0} documents deleted'.format(device_document))
    else:
        print(f'{username} does not have permission to delete data for {deviceid}')


# Access validation and operations on WeatherData Collection

wdata_coll = WeatherDataModel()


# The below code demonstrates successful and unsuccessful read on weather_data collection
# based on device access as per alist field of the user. If user in the "username" has 'r' or 'rw' access for the
# "device_id", proceed with search of the record in the weather_data collection else return permission denied

# Input for successful read of weather data
# username = "user_2"
# deviceid = "DT001"

# #Input for unsuccessful read of weather data
username = "user_2"
deviceid = "DH005"


device_access = wdata_coll.validate_permission(username, deviceid)
if (device_access == -1):
    print(wdata_coll.latest_error)
    exit()
else:
    print('Weather data read:')
    if (device_access in ('r', 'rw')):
        wdata_document = wdata_coll.find_by_device_id_and_timestamp(deviceid, datetime(2020, 12, 1, 2, 30, 0))
        if (wdata_document == -1):
            print('Data does not exist')
        else:
            print(wdata_document)
    else:
        print(f'{username} does not have permission to access data for {deviceid}')


# The below code demonstrates successful and unsuccessful insert on weather data collection
# based on device access as per alist field of the user. If user in the "username" has 'w' or 'rw' access for the
# "deviceid", proceed with insertion of the record in the weather data collection else return permission denied

# Input for successful read of weather data
# username = "user_2"
# deviceid = "DT100"

# #Input for unsuccessful read of weather data
username = "user_2"
deviceid = "DH005"


device_access = wdata_coll.validate_permission(username, deviceid)
if (device_access == -1):
    print(wdata_coll.latest_error)
else:
    print('Insert weather data:')
    if (device_access in ('w', 'rw')):
        wdata_document = wdata_coll.insert(deviceid, 25, datetime(2020, 12, 1, 2, 30, 0))
        if (wdata_document == -1):
            print(wdata_coll.latest_error)
        else:
            print(wdata_document)
    else:
        print(f'{username} does not have permission to insert data for the device {deviceid}')


# The below code demonstrates successful and unsuccessful update on weather_data collection
# based on device access as per alist field of the user. If user in the "username" has 'w' or 'rw' access for the
# "deviceid", proceed with update of the record in the weather_data collection else return permission denied

# Input for successful update of weather data
# username = "user_2"
# deviceid = "DT100"

# #Input for unsuccessful update of weather data
username = "user_2"
deviceid = "DH005"

device_access = wdata_coll.validate_permission(username, deviceid)
if (device_access == -1):
    print(wdata_coll.latest_error)
else:
    print('Update device data:')
    if (device_access in ('w', 'rw')):
        wdata_document = wdata_coll.update(deviceid, datetime(2020, 12, 1, 2, 30, 0), 32)
        if (wdata_document == -1):
            print(wdata_coll.latest_error)
        else:
            print(wdata_document)
    else:
        print(f'{username} does not have permission to update data for {deviceid}')

# The below code demonstrates successful and unsuccessful deletion on weather_data collection
# based on device access as per alist field of the user. If user in the "username" has 'w' or 'rw' access for the
# "deviceid", proceed with deletion of the record in the weather_data collection else return permission denied

# Input for successful deletion of weather data
# username = "user_2"
# deviceid = "DT100"

# #Input for unsuccessful deletion of weather data
username = "user_2"
deviceid = "DH005"

print('Delete weather data:')
device_access = wdata_coll.validate_permission(username, deviceid)
if (device_access == -1):
    print(wdata_coll.latest_error)
else:
    if (device_access in ('w', 'rw')):
        wdata_document = wdata_coll.delete(deviceid, datetime(2020, 12, 1, 2, 30, 0))
        if (wdata_document == -1):
            print(wdata_coll.latest_error)
        else:
            print('{0} documents deleted'.format(wdata_document))
    else:
        print(f'{username} does not have permission to delete data for {deviceid}')



# Daily Reports Aggregation and Retrieval:

print('Daily Report Aggregation')
daily_report_coll = DailyReportModel()

dr_document = daily_report_coll.data_aggregator()
print(dr_document)

# # Retrieve daily report for a date range and device

print('Daily Report Retrieval:')
device_id = 'DT002'
from_date = '01-12-2020'
to_date = '06-12-2020'

dr_document = daily_report_coll.find_daily_data(device_id, from_date, to_date)
for doc in dr_document:
    print(doc)






