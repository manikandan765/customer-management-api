import requests
import hmac
import hashlib
import json

url = "http://127.0.0.1:8000/webhooks/customer-events"
secret = "supersecretwebhookkey"
payload = {"event": "customer.created", "data": {"id": 1, "name": "Jane Doe"}}
body = json.dumps(payload).encode('utf-8')

# 1. Test Valid Signature
valid_sig = hmac.new(secret.encode('utf-8'), body, hashlib.sha256).hexdigest()
res = requests.post(url, json=payload, headers={"X-Signature": valid_sig})
print(f"Valid Signature: {res.status_code} -> {res.json()}")

# 2. Test Tampered Payload
res = requests.post(url, json=payload, headers={"X-Signature": "bad_signature"})
print(f"Tampered Payload: {res.status_code} -> {res.json()}")

# 3. Test Missing Signature
res = requests.post(url, json=payload)
print(f"Missing Signature: {res.status_code} -> {res.json()}")