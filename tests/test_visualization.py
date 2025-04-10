# tests/test_visualization.py
import unittest
import os
from src.database import Database
from src.visualization import visualize_laureates_by_country
from src.config import Config

class TestVisualization(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.collection = self.db.get_collection('test_viz_collection')
        self.collection.insert_many([
            {'bornCountry': 'USA'},
            {'bornCountry': 'UK'}
        ])
    
    def test_visualization(self):
        visualize_laureates_by_country(self.collection)
        self.assertTrue(os.path.exists(Config.VISUALIZATION_OUTPUT))
        os.remove(Config.VISUALIZATION_OUTPUT)
    
    def tearDown(self):
        self.collection.drop()
        self.db.close()

if __name__ == '__main__':
    unittest.main()