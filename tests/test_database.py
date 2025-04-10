# tests/test_database.py
import unittest
from src.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()
    
    def test_connection(self):
        self.assertTrue(self.db.test_connection())
    
    def test_extract_laureates(self):
        laureates = self.db.extract_laureates()
        self.assertIsInstance(laureates, list)
    
    def tearDown(self):
        self.db.close()

if __name__ == '__main__':
    unittest.main()