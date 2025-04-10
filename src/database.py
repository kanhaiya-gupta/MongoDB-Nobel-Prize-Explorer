# src/database.py
from pymongo import MongoClient
from src.config import Config

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI, serverSelectionTimeoutMS=5000)
        self.db = self.client[Config.DATABASE_NAME]
    
    def test_connection(self):
        try:
            self.client.admin.command('ping')
            print("Connected to MongoDB successfully!")
            return True
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            return False
    
    def extract_laureates(self):
        collection = self.db[Config.SOURCE_LAUREATES_COLLECTION]
        laureates = list(collection.find({}))
        print(f"Extracted {len(laureates)} laureates.")
        return laureates
    
    def get_collection(self, collection_name):
        return self.db[collection_name]
    
    def close(self):
        self.client.close()