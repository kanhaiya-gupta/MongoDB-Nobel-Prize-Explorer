# tests/test_transform.py
import unittest
from src.transform import transform_data

class TestTransform(unittest.TestCase):
    def test_transform_data(self):
        sample_data = [{
            'id': '1',
            'firstname': 'Test',
            'surname': 'Person',
            'born': '1900-01-01',
            'died': '0000-00-00',
            'bornCountry': 'Testland',
            'gender': 'male',
            'prizes': [{'year': '1920', 'category': 'physics', 'share': '1'}]
        }]
        transformed = transform_data(sample_data)
        self.assertEqual(len(transformed), 1)
        self.assertEqual(transformed[0]['total_prizes'], 1)
        self.assertEqual(transformed[0]['prizes'][0]['age_at_award'], 20)
        self.assertIsNone(transformed[0]['died'])

if __name__ == '__main__':
    unittest.main()