# Imports Database class from the project to provide basic functionality for database access
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId
from datetime import datetime


# User document contains username (String), email (String), and role (String) fields
class UserModel:
    USER_COLLECTION = 'users'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since username should be unique in users collection, this provides a way to fetch the user document based on the username
    def find_by_username(self, username):
        key = {'username': username}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        user_document = self._db.get_single_data(UserModel.USER_COLLECTION, key)
        if (user_document):
            return user_document
        else:
            return -1
    
    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, username, email, role,alist):
        self._latest_error = ''
        user_document = self.find_by_username(username)
        if (user_document != -1):
            self._latest_error = f'Record for {username} already exists'
            return -1

        user_data = {'username': username, 'email': email, 'role': role, 'alist': alist}
        user_obj_id = self._db.insert_single_data(UserModel.USER_COLLECTION, user_data)
        return self.find_by_object_id(user_obj_id)

    # The function reads the user record from user collection. If there is no records return error.
    # If record exists checks for the role of the user. If the role is admin return True else return the
    # error for access denied.

    def validate_permission(self, username):
        self._latest_error = ''
        key = {'username': username}
        user_document = self.find_by_username(username)
        if(user_document != -1):
            if (user_document['role'] == 'admin'):
                return True
            else:
                self._latest_error = f'User {username} does not have access to data'
                return -1
        else:
            self._latest_error = f'User {username} does not exist'
            return -1

    # The function first checks if the record for key exists in User collection. Return error if no
    # record for the username exists. If record exists proceeds with update of the data and return the record updated.

    def update(self, key, user_data):
        self._latest_error = ''
        user_document = self.find_by_username(key)

        if (user_document == -1):
            self._latest_error = f'Record for {key} does not exist'
            return -1

        filter = {'username': key}
        data = {}
        if ('alist' in user_data):
            alist_data = user_data.pop('alist')
            data['$addToSet'] = {'alist': { '$each': alist_data}}
        if(user_data):
            data['$set'] = user_data
        result = self._db.update_single_data(UserModel.USER_COLLECTION, filter, data)
        if (result):
                return self.find_by_username(key)

    # The function first checks if the record for username exists in User collection. Return error if no
    # record for the username exists. If record exists delete the record and return the count of documents deleted

    def delete(self, username):
        self._latest_error = ''
        user_document = self.find_by_username(username)
        if (user_document == -1):
            self._latest_error = f'Record for {username} does not exist'
            return -1

        user_data = {'username': username}
        d_count = self._db.delete_single_data(UserModel.USER_COLLECTION, user_data)
        return d_count



# Device document contains device_id (String), desc (String), type (String - temperature/humidity) and manufacturer (String) fields
class DeviceModel:
    DEVICE_COLLECTION = 'devices'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id should be unique in devices collection, this provides a way to fetch the device document based on the device id
    def find_by_device_id(self, device_id):
        key = {'device_id': device_id}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        device_document = self._db.get_single_data(DeviceModel.DEVICE_COLLECTION, key)
        return device_document
    
    # This first checks if a device already exists with that device id. If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, desc, type, manufacturer):
        self._latest_error = ''
        device_document = self.find_by_device_id(device_id)
        if (device_document):
            self._latest_error = f'Device id {device_id} already exists'
            return -1

        device_data = {'device_id': device_id, 'desc': desc, 'type': type, 'manufacturer': manufacturer}
        device_obj_id = self._db.insert_single_data(DeviceModel.DEVICE_COLLECTION, device_data)
        return self.find_by_object_id(device_obj_id)

    def validate_permission(self, username, device_id):
        user_col = UserModel()
        self._latest_error = ''
        device_document = user_col.find_by_username(username)
        if(device_document != -1):
            access = ""
            if ('alist' in device_document):
                for item in device_document['alist']:
                    if (device_id in item):
                        access = item[device_id]
                        break;
                return access
        else:
            self._latest_error = f'No device access data for {username}:{device_id} '
            return -1

    def update(self, key, user_data):
        self._latest_error = ''
        device_document = self.find_by_device_id(key)

        if (device_document == -1):
            self._latest_error = f'Record for {key} does not exist'
            return -1

        filter = {'device_id': key}
        data = {'$set': user_data}
        result = self._db.update_single_data(DeviceModel.DEVICE_COLLECTION, filter, data)
        if (result):
                return self.find_by_device_id(key)

    # The function first checks if the record for device exists in Device collection. Return error if no
    # record for the device exists. If record exists delete the record and return the count of documents deleted

    def delete(self, device_id):
        self._latest_error = ''
        device_document = self.find_by_device_id(device_id)
        if (device_document == -1):
            self._latest_error = f'Record for {device_id} does not exist'
            return -1

        user_data = {'device_id': device_id}
        d_count = self._db.delete_single_data(DeviceModel.DEVICE_COLLECTION, user_data)
        return d_count



# Weather data document contains device_id (String), value (Integer), and timestamp (Date) fields
class WeatherDataModel:
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''
    
    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error
    
    # Since device id and timestamp should be unique in weather_data collection, this provides a way to fetch the data document based on the device id and timestamp
    def find_by_device_id_and_timestamp(self, device_id, timestamp):
        key = {'device_id': device_id, 'timestamp': timestamp}
        return self.__find(key)
    
    # Finds a document based on the unique auto-generated MongoDB object id 
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)
    
    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        wdata_document = self._db.get_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, key)
        if (wdata_document):
            return wdata_document
        else:
            return -1
    
    # This first checks if a data item already exists at a particular timestamp for a device id. If it does, it populates latest_error and returns -1.
    # If it doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, value, timestamp):
        self._latest_error = ''
        wdata_document = self.find_by_device_id_and_timestamp(device_id, timestamp)
        if (wdata_document != -1):
            self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
            return -1
        
        weather_data = {'device_id': device_id, 'value': value, 'timestamp': timestamp}
        wdata_obj_id = self._db.insert_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, weather_data)
        return self.find_by_object_id(wdata_obj_id)

    def validate_permission(self, username, device_id):
        user_col = UserModel()
        self._latest_error = ''
        wdata_document = user_col.find_by_username(username)
        if (wdata_document != -1):
            access = ""
            if ('alist' in wdata_document):
                for item in wdata_document['alist']:
                    if (device_id in item):
                        access = item[device_id]
                        break;
                return access
        else:
            self._latest_error = f'No device access data for {username}:{device_id} '
            return -1

    def update(self, key, time_stamp, value):
        self._latest_error = ''
        wdata_document = self.find_by_device_id_and_timestamp(key, time_stamp)

        if (wdata_document == -1):
            self._latest_error = f'Record for {key} does not exist'
            return -1

        filter = {'device_id': key, 'timestamp': time_stamp}
        data = {'$set': {'value': value}}
        result = self._db.update_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, filter, data)
        if (result):
                return self.find_by_device_id_and_timestamp(key, time_stamp)

    def delete(self, key, time_stamp):
        self._latest_error = ''
        wdata_document = self.find_by_device_id_and_timestamp(key, time_stamp)
        if (wdata_document == -1):
            self._latest_error = f'Record for {key} does not exist'
            return -1

        user_data = {'device_id': key, 'timestamp': time_stamp}
        d_count = self._db.delete_single_data(WeatherDataModel.WEATHER_DATA_COLLECTION, user_data)
        return d_count


class DailyReportModel:

    DAILY_REPORT_COLLECTION = 'daily_reports'
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self):
        self._db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error


    def data_aggregator(self):
        self._latest_error = ''

        pipeline1 = [{'$group': {'_id': {'device_id': '$device_id',
                                         'day': {'$dateToString': {'format': '%d-%m-%Y', 'date': '$timestamp'}}},
                      'average': {'$avg': '$value'}, 'maximum': {'$max': '$value'}, 'minimum': {'$min': '$value'}}},
                     {'$sort': {'_id': 1}}]

        result = self._db.aggregate_data(DailyReportModel.WEATHER_DATA_COLLECTION, pipeline1)
        data_list = []
        for doc in result:
            data = {}
            for i, (j, k) in enumerate(doc.items()):
                if (j == '_id'):
                    data['device_id'] = k['device_id']
                    data['day'] = datetime.strptime(k['day'],  "%d-%m-%Y")
                else:
                    data[j] = k
            data_list.append(data)
        dr_document = self._db.drop_collection(DailyReportModel.DAILY_REPORT_COLLECTION)
        drdata_obj_id = self._db.insert_multiple_data(DailyReportModel.DAILY_REPORT_COLLECTION, data_list)
        return drdata_obj_id


    def find_daily_data(self, deviceid, fromdate, todate):
        self._latest_error = ''

        from_date = datetime.strptime(fromdate,  "%d-%m-%Y")
        to_date = datetime.strptime(todate,  "%d-%m-%Y")
        key = {'device_id': deviceid, 'day': {'$gte': from_date, '$lte': to_date}}

        drdata_obj_id = self._db.find_multiple_data(DailyReportModel.DAILY_REPORT_COLLECTION, key)
        return drdata_obj_id









