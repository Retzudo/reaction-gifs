import gifs
import unittest
import yaml


class TestCase(unittest.TestCase):
    def setUp(self):
        self.client = gifs.app.test_client()

    def test_yaml(self):
        """Test if YAML file is valid."""
        with open('gifs.yaml') as f:
            yaml.load(f.read())

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_gifs(self):
        response = self.client.get('/gifs.json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

    def test_https(self):
        """Test if all gif URLs are HTTPS URLs."""
        data = []
        with open('gifs.yaml') as f:
            data = yaml.load(f.read())

        for gif in data['gifs']:
            self.assertTrue(gif['url'].startswith('https'))


if __name__ == '__main__':
    unittest.main()
