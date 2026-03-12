import httpx
import json
import sys

BASE_URL = "http://localhost:8000"
TIMEOUT = 6000

response = httpx.post(
    f"{BASE_URL}/api/v1/ease",
    json={
        "request": "Our startup needs to decide whether to open-source our core ML model. "
        "We have 50 employees, $2M runway, and 3 enterprise clients who rely on our proprietary advantage. "
        "Our competitors are catching up fast.",
        "context": {
            "company_size": 50,
            "runway_usd": 2000000,
            "enterprise_clients": 3,
            "industry": "machine learning",
            "competitor_threat": "high",
        },
        "min_actions": 5,
    },
    timeout=TIMEOUT,
)

print(f"Status: {response.status_code}")
data = response.json()
print(json.dumps(data, indent=2))
if response.status_code != 200:
    sys.exit(1)
