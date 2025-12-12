from fastapi import APIRouter, HTTPException, status
from app.schemas.organization import AdminLoginRequest, AdminLoginResponse
from app.services.organization_service import OrganizationService

router = APIRouter(prefix="/admin", tags=["authentication"])


@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(request: AdminLoginRequest):
    """Admin login endpoint"""
    try:
        result = await OrganizationService.authenticate_admin(
            email=request.email,
            password=request.password
        )
        return AdminLoginResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

