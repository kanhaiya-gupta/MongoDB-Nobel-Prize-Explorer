# import os
# from bson import json_util
# from src.database import Database
# from src.config import Config

# def extract():
#     db = Database()

#     if not db.test_connection():
#         raise ConnectionError("MongoDB connection failed.")

#     laureates = db.extract_laureates()
#     db.close()

#     output_path = Config.OUTPUT_PATH
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

#     with open(output_path, "w", encoding="utf-8") as f:
#         json_str = json_util.dumps(laureates, indent=4)
#         f.write(json_str)

#     print(f"✅ Extracted {len(laureates)} laureates to {output_path}")



# if __name__ == "__main__":
#     extract()


import pymongo
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_data():
    logger.info("Starting extract step")
    uri = os.getenv("MONGODB_URI", "mongodb://mongodb-service:27017/")
    logger.info(f"Connecting to MongoDB at {uri}")
    try:
        client = pymongo.MongoClient(uri)
        db = client["nobel"]
        logger.info("Connected to database 'nobel'")
        laureates = list(db["laureates"].find())
        logger.info(f"Retrieved {len(laureates)} laureates")
        output_path = "/data/extracted_laureates.json"
        logger.info(f"Writing to {output_path}")
        with open(output_path, "w") as f:
            json.dump(laureates, f)
        logger.info("Extract completed successfully")
    except Exception as e:
        logger.error(f"Error in extract: {str(e)}")
        raise

if __name__ == "__main__":
    extract_data()