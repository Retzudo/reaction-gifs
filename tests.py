import gifs
import unittest
import yaml


class TestCase(unittest.TestCase):
    def setUp(self):
        self.client = gifs.app.test_client()

    def test_yaml(self):
        """Test if YAML file is valid."""
        with open('gifs.yml') as f:
            yaml.load(f.read())

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_gifs(self):
        response = self.client.get('/gifs.json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')


if __name__ == '__main__':
    unittest.main()
