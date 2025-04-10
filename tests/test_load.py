# tests/test_load.py
import unittest
from src.database import Database
from src.load import load_data

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.collection_name = 'test_load_collection'
    
    def test_load_data(self):
        sample_data = [{'_id': '1', 'name': 'Test'}]
        collection = load_data(self.db, sample_data, self.collection_name)
        self.assertEqual(collection.count_documents({}), 1)
    
    def tearDown(self):
        self.db.get_collection(self.collection_name).drop()
        self.db.close()

if __name__ == '__main__':
    unittest.main()