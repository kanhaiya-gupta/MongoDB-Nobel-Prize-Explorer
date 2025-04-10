# main.py
from src.database import Database
from src.transform import transform_data
from src.load import load_data
from src.visualization import visualize_laureates_by_country
from src.config import Config

def main():
    db = Database()
    if not db.test_connection():
        print("Exiting due to connection failure.")
        return
    
    raw_laureates = db.extract_laureates()
    transformed_laureates = transform_data(raw_laureates)
    transformed_collection = load_data(db, transformed_laureates)
    
    num_prizes = db.get_collection(Config.SOURCE_PRIZES_COLLECTION).count_documents({})
    num_laureates = db.get_collection(Config.SOURCE_LAUREATES_COLLECTION).count_documents({})
    print(f"Number of prizes: {num_prizes}")
    print(f"Number of laureates: {num_laureates}")
    print("TRUE: There are more laureates than prizes" if num_laureates > num_prizes else "TRUE: There are more prizes than laureates or equal")
    
    visualize_laureates_by_country(transformed_collection)
    db.close()

if __name__ == "__main__":
    main()