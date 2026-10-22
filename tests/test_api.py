import hmac
import hashlib
import json

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_customer_201(client):
    response = client.post("/customers", json={
        "name": "Test User", 
        "email": "test@example.com", 
        "phone": "1234567890", 
        "city": "TestCity"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test User"
    assert response.json()["email"] == "test@example.com"

def test_create_customer_invalid_email_422(client):
    # 422 Unprocessable Entity for invalid Pydantic validation (bad email)
    response = client.post("/customers", json={
        "name": "Bad User", 
        "email": "not-an-email", 
        "phone": "123", 
        "city": "TestCity"
    })
    assert response.status_code == 422

def test_duplicate_email_409(client):
    # Try to create another user with the same email
    response = client.post("/customers", json={
        "name": "Test User 2", 
        "email": "test@example.com"
    })
    assert response.status_code == 409
    assert "Email already registered" in response.json()["detail"]

def test_get_unknown_id_404(client):
    response = client.get("/customers/999")
    assert response.status_code == 404
    assert "Customer not found" in response.json()["detail"]

def test_get_customers_with_pagination(client):
    response = client.get("/customers?page=1&per_page=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_webhook_valid_signature(client):
    payload = {"event": "customer.created", "data": {"id": 1}}
    body = json.dumps(payload).encode('utf-8')
    secret = b"supersecretwebhookkey"
    sig = hmac.new(secret, body, hashlib.sha256).hexdigest()
    
    response = client.post("/webhooks/customer-events", content=body, headers={"X-Signature": sig})
    assert response.status_code == 200
    assert response.json() == {"status": "accepted"}

def test_webhook_tampered_payload_401(client):
    payload = {"event": "customer.created", "data": {"id": 1}}
    body = json.dumps(payload).encode('utf-8')
    
    response = client.post("/webhooks/customer-events", content=body, headers={"X-Signature": "bad_signature"})
    assert response.status_code == 401
    assert "Invalid signature" in response.json()["detail"]

def test_webhook_missing_signature_401(client):
    payload = {"event": "customer.created", "data": {"id": 1}}
    body = json.dumps(payload).encode('utf-8')
    
    response = client.post("/webhooks/customer-events", content=body)
    assert response.status_code == 401
    assert "Missing signature" in response.json()["detail"]