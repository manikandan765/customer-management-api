import os
from dotenv import load_dotenv
from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader

load_dotenv()
VALID_API_KEY = os.getenv("API_KEY")

# This tells Swagger UI to treat this as a security scheme
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return api_key