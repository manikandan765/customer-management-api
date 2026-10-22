import os
import hmac
import hashlib
import json

from dotenv import load_dotenv
from fastapi import APIRouter, Request, BackgroundTasks, HTTPException, Header

load_dotenv()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

router = APIRouter()

def process_event_in_background(event_data: dict):
    """This runs in the background after the 200 OK is sent."""
    print(f"🚀 [Background Task] Processing event: {event_data.get('event')}")

@router.post("/webhooks/customer-events")
async def receive_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_signature: str = Header(None, alias="X-Signature")
):
    # 1. Check if signature is missing
    if not x_signature:
        raise HTTPException(status_code=401, detail="Missing signature")

    # 2. Read the raw request body
    body = await request.body()

    # 3. Calculate the expected HMAC-SHA256 signature
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'), 
        body, 
        hashlib.sha256
    ).hexdigest()

    # 4. Validate using compare_digest (prevents timing attacks)
    if not hmac.compare_digest(expected_signature, x_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # 5. Parse the JSON body to pass to the background task
    event_data = json.loads(body)
    
    # 6. Add the background task and return 200 immediately
    background_tasks.add_task(process_event_in_background, event_data)
    
    return {"status": "accepted"}