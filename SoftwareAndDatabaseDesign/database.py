# Imports MongoClient for base level access to the local MongoDB
from pymongo import MongoClient


class Database:
    # Class static variables used for database host ip and port information, database name
    # Static variables are referred to by using <class_name>.<variable_name>
    HOST = 'localhost'
    PORT = '27017'
    DB_NAME = 'weather_db'

    def __init__(self):
        self._db_conn = MongoClient(f'mongodb://{Database.HOST}:{Database.PORT}')
        self._db = self._db_conn[Database.DB_NAME]
    
    # This method finds a single document using field information provided in the key parameter
    # It assumes that the key returns a unique document. It returns None if no document is found
    def get_single_data(self, collection, key):
        db_collection = self._db[collection]
        document = db_collection.find_one(key)
        return document
    
    # This method inserts the data in a new document. It assumes that any uniqueness check is done by the caller
    def insert_single_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.insert_one(data)
        return document.inserted_id

    def update_single_data(self, collection, key, data):
        db_collection = self._db[collection]
        document = db_collection.update_one(key, data)
        return document.acknowledged

    def aggregate_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.aggregate(data)
        return document

    def insert_multiple_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.insert(data)
        return document

    def drop_collection(self, collection):
        db_collection = self._db[collection]
        document = db_collection.drop()
        return document

    def find_multiple_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.find(data)
        return document

    def delete_single_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.delete_one(data)
        return document.deleted_count
    