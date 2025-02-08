
from pymongo import MongoClient
import pandas as pd

# MongoDB Connection
class MongoDB:
    """
    """
    def __init__(self, username=None, password=None):
        if username and password:
            # Authenticated connection string
            url = f"mongodb+srv://{username}:{password}@cluster0.sst2o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            self.client = MongoClient(url)

        else:
            # rais error 
            raise ValueError("Username and password are required.")
        

    def get_data(self, db_name, collection_name, query=None, projection=None):
        """
        Retrieve data from a MongoDB collection.
        db_name: str, name of the database.
        collection_name: str, name of the collection.
        query: dict, query to filter documents.
        projection: dict, fields to include or exclude.
        """
        if query is None:
            query = {}
        cursor = self.client[db_name][collection_name].find_one(query, projection)
        return cursor

    def update_data(self, db_name, collection_name, query, update):
        """
        Update a document in the MongoDB collection.
        query: dict, the filter for the document to update.
        update: dict, the update operation.
        """
        result = self.client[db_name][collection_name].update_one(query, update)
        return result.modified_count
    
    def insert_data(self, db_name, collection_name, data):
        """
        Insert data into a MongoDB collection.
        db_name: str, name of the database.
        collection_name: str, name of the collection.
        data: dict or list of dict, data to insert.
        """
        if isinstance(data, list):
            result = self.client[db_name][collection_name].insert_many(data)
        else:
            result = self.client[db_name][collection_name].insert_one(data)
        return result.inserted_id
    
