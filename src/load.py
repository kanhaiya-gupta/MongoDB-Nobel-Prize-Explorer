# src/load.py
from src.config import Config

def load_data(db, transformed_laureates, collection_name=Config.TARGET_COLLECTION):
    collection = db.get_collection(collection_name)
    collection.drop()
    if transformed_laureates:
        collection.insert_many(transformed_laureates)
        print(f"Loaded {len(transformed_laureates)} documents into '{collection_name}'.")
    else:
        print("No data to load.")
    return collection