# src/config.py
import os

class Config:
    MONGODB_URI = "mongodb://localhost:27017/"
    DATABASE_NAME = "nobel"
    SOURCE_LAUREATES_COLLECTION = "laureates"
    SOURCE_PRIZES_COLLECTION = "prizes"
    TARGET_COLLECTION = "laureates_transformed"
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # Root directory
    RESULTS_DIR = os.path.join(BASE_DIR, 'results')
    VISUALIZATION_OUTPUT = os.path.join(RESULTS_DIR, "laureates_by_country.png")