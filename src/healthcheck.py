import requests
import sys

try:
    response = requests.get('http://localhost:6006/api/v1/health', timeout=3)
    response.raise_for_status()
except requests.RequestException:
    sys.exit(1)
