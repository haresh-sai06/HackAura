import requests
import json

response = requests.get('http://localhost:8000/api/calls')
calls = response.json()
print(f'Found {len(calls)} calls')
print(json.dumps(calls, indent=2))
