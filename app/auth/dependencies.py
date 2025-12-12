from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import JWTHandler
from typing import Optional

security = HTTPBearer()


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Dependency to get current authenticated admin from JWT token"""
    token = credentials.credentials
    payload = JWTHandler.decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    admin_id: str = payload.get("sub")
    organization_name: str = payload.get("organization_name")
    token_type: str = payload.get("type")
    
    if admin_id is None or organization_name is None or token_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "admin_id": admin_id,
        "organization_name": organization_name
    }


async def verify_org_access(
    organization_name: str,
    current_admin: dict = Depends(get_current_admin)
) -> dict:
    """Verify that the current admin has access to the specified organization"""
    if current_admin["organization_name"] != organization_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this organization"
        )
    return current_admin

