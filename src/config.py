# src/config.py
class Config:
    MONGODB_URI = "mongodb://localhost:27017/"
    DATABASE_NAME = "nobel"
    SOURCE_LAUREATES_COLLECTION = "laureates"
    SOURCE_PRIZES_COLLECTION = "prizes"
    TARGET_COLLECTION = "laureates_transformed"
    VISUALIZATION_OUTPUT = "laureates_by_country.png"