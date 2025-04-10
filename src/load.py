# src/load.py
from src.config import Config
from pymongo.errors import BulkWriteError

def load_data(db, transformed_laureates, collection_name=Config.TARGET_COLLECTION):
    collection = db.get_collection(collection_name)
    collection.drop()  # Clear existing data
    if not transformed_laureates:
        print("No data to load.")
        return collection
    
    try:
        result = collection.insert_many(transformed_laureates, ordered=False)
        print(f"Loaded {len(result.inserted_ids)} documents into '{collection_name}'.")
    except BulkWriteError as bwe:
        write_errors = bwe.details.get('writeErrors', [])
        inserted_count = bwe.details.get('nInserted', 0)
        print(f"Loaded {inserted_count} documents into '{collection_name}' with {len(write_errors)} errors.")
        for error in write_errors:
            print(f"Error at index {error['index']}: {error['errmsg']}, duplicate key: {error['keyValue']}")
    
    return collection