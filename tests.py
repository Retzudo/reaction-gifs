import gifs
import json
import unittest


class TestCase(unittest.TestCase):
	def setUp(self):
		self.client = gifs.app.test_client()

	def test_json(self):
		"""Test if JSON file is valid."""
		with open('gifs.json') as f:
			json.loads(f.read())

	def test_index(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_gifs(self):
		response = self.client.get('/gifs')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.mimetype, 'application/json')


if __name__ == '__main__':
	unittest.main()
