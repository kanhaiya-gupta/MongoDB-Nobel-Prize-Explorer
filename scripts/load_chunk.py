import json
from src.load import load_data
from src.config import Config
from src.database import Database

def load_chunk():
    input_path = os.environ["INPUT_PATH"]
    with open(input_path, "r") as f:
        transformed_laureates = json.load(f)
    
    db = Database()
    collection = load_data(db, transformed_laureates)
    db.close()
    print(f"Loaded {len(transformed_laureates)} documents from {input_path}")

if __name__ == "__main__":
    load_chunk()