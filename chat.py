"""Local Ollama chat bridge; conversation history is supplied by the browser."""
import json
import socket
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from flask import Blueprint, request

chat_api = Blueprint('chat', __name__)


@chat_api.post('/api/chat')
def chat():
    body = request.get_json(silent=True)
    messages = body.get('messages') if isinstance(body, dict) else None
    if not isinstance(messages, list) or not 1 <= len(messages) <= 40:
        return {'error': 'Send between 1 and 40 messages.'}, 400
    for message in messages:
        if not isinstance(message, dict) or message.get('role') not in ('user', 'assistant') or not isinstance(message.get('content'), str) or not 1 <= len(message['content'].strip()) <= 4000:
            return {'error': 'Messages must contain text of 1–4000 characters.'}, 400
    if messages[-1]['role'] != 'user':
        return {'error': 'The final message must be from the user.'}, 400
    payload = {'model': 'llama3.2:3b', 'stream': False, 'messages': [
        {'role': m['role'], 'content': m['content']} for m in messages
    ], 'options': {'num_predict': 700, 'num_ctx': 8192}}
    call = Request('http://127.0.0.1:11434/api/chat', data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
    try:
        with urlopen(call, timeout=180) as response:
            data = json.load(response)
        content = data.get('message', {}).get('content')
        if not isinstance(content, str) or not content.strip():
            return {'error': 'Ollama returned an empty reply. Please try again.'}, 502
        return {'message': content, 'model': 'llama3.2:3b'}, 200, {'Cache-Control': 'no-store'}
    except HTTPError as error:
        if error.code == 404:
            return {'error': 'Model missing. Run: ollama pull llama3.2:3b'}, 503
        return {'error': 'Ollama could not generate a reply. Please try again.'}, 502
    except (TimeoutError, socket.timeout):
        return {'error': 'Ollama took too long. Try a shorter message.'}, 504
    except URLError:
        return {'error': 'Ollama is offline. Start it with: ollama serve'}, 503
    except (ValueError, AttributeError):
        return {'error': 'Ollama returned an unexpected response.'}, 502
