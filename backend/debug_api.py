import requests
import traceback

try:
    response = requests.get('http://localhost:8000/api/calls', timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
