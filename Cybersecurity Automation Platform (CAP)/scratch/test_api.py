import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import create_app

def test_api():
    app = create_app()
    app.testing = True
    client = app.test_client()

    print("Testing Root Endpoint...")
    res = client.get('/')
    print(f"Status: {res.status_code}, Data: {res.get_json()}")

    print("\nTesting AI Analyze URL...")
    res = client.post('/api/ai/analyze-url', json={"url": "http://malicious-site.com"})
    print(f"Status: {res.status_code}, Data: {res.get_json()}")

    print("\nTesting Get Alerts...")
    res = client.get('/api/alerts/')
    print(f"Status: {res.status_code}, Data: {res.get_json()}")

if __name__ == "__main__":
    test_api()
