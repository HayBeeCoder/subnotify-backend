from fastapi import Depends, HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # Extract token
    if not token:  # Replace with actual validation logic
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"username": "test_user"}