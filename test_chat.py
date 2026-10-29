import io
import json
import unittest
from unittest.mock import patch
from urllib.error import URLError, HTTPError
from main import app


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.payload = {'messages': [{'role': 'user', 'content': 'Hello'}]}

    @patch('chat.urlopen')
    def test_success_and_history(self, call):
        call.return_value = io.BytesIO(json.dumps({'message': {'content': 'Hello back'}}).encode())
        response = self.client.post('/api/chat', json=self.payload, headers={'Origin': 'null'})
        self.assertEqual(response.json['message'], 'Hello back')
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'null')
        sent = json.loads(call.call_args.args[0].data)
        self.assertEqual(sent['model'], 'llama3.2:3b')
        self.assertEqual(sent['messages'], self.payload['messages'])

    def test_validation(self):
        for payload in [None, {}, {'messages': []}, {'messages': [{'role': 'system', 'content': 'x'}]}, {'messages': [{'role': 'user', 'content': 'x' * 4001}]}]:
            self.assertEqual(self.client.post('/api/chat', json=payload).status_code, 400)

    @patch('chat.urlopen')
    def test_errors(self, call):
        for error, status in [(URLError('offline'), 503), (TimeoutError(), 504), (HTTPError('url', 404, 'missing', {}, None), 503)]:
            call.side_effect = error
            self.assertEqual(self.client.post('/api/chat', json=self.payload).status_code, status)


if __name__ == '__main__':
    unittest.main()
