import unittest
from main import app


class OutfitTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.profile = dict(height=175, weight='', color='olive', occasion='Everyday', fit='Relaxed', weather='Mild')

    def test_preferences_change_outfit(self):
        first = self.client.post('/api/outfit', json=self.profile)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(len(first.json['items']), 3)
        second = self.client.post('/api/outfit', json={**self.profile, 'occasion': 'Office', 'color': 'navy', 'weather': 'Cool', 'height': 190})
        self.assertEqual(second.status_code, 200)
        self.assertNotEqual(first.json['items'], second.json['items'])
        self.assertIn('tall-length', second.json['notes'][1])
        self.assertEqual(second.headers['Cache-Control'], 'no-store')

    def test_bad_input(self):
        for changes in [dict(height='abc'), dict(height=0), dict(weight=-1), dict(color=[]), dict(fit='bad'), dict(height=True)]:
            response = self.client.post('/api/outfit', json={**self.profile, **changes})
            self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.post('/api/outfit', json=[]).status_code, 400)

    def test_standalone_cors(self):
        response = self.client.options('/api/outfit', headers={'Origin': 'null', 'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': 'content-type'})
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'null')
        self.assertIn('POST', response.headers['Access-Control-Allow-Methods'])
        response = self.client.post('/api/outfit', json=self.profile, headers={'Origin': 'null'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'null')


if __name__ == '__main__':
    unittest.main()
