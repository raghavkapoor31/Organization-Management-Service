from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.organization import (
    OrganizationCreateRequest,
    OrganizationGetRequest,
    OrganizationUpdateRequest,
    OrganizationDeleteRequest,
    OrganizationResponse,
    AdminLoginRequest,
    AdminLoginResponse
)
from app.services.organization_service import OrganizationService
from app.auth.dependencies import get_current_admin, verify_org_access

router = APIRouter(prefix="/org", tags=["organizations"])


@router.post("/create", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(request: OrganizationCreateRequest):
    """Create a new organization with admin user"""
    try:
        result = await OrganizationService.create_organization(
            organization_name=request.organization_name,
            email=request.email,
            password=request.password
        )
        return OrganizationResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create organization: {str(e)}"
        )


@router.get("/get", response_model=OrganizationResponse)
async def get_organization(request: OrganizationGetRequest):
    """Get organization details by name"""
    try:
        result = await OrganizationService.get_organization(request.organization_name)
        return OrganizationResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get organization: {str(e)}"
        )


@router.put("/update", response_model=OrganizationResponse)
async def update_organization(
    request: OrganizationUpdateRequest,
    current_admin: dict = Depends(get_current_admin)
):
    """Update organization (admin credentials and optionally rename organization)"""
    try:
        # Verify admin has access to this organization
        await verify_org_access(request.organization_name, current_admin)
        
        result = await OrganizationService.update_organization(
            organization_name=request.organization_name,
            new_email=request.email,
            new_password=request.password,
            current_admin=current_admin,
            new_organization_name=request.new_organization_name
        )
        return OrganizationResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update organization: {str(e)}"
        )


@router.delete("/delete")
async def delete_organization(
    request: OrganizationDeleteRequest,
    current_admin: dict = Depends(get_current_admin)
):
    """Delete organization (authenticated admin only)"""
    try:
        # Verify admin has access to this organization
        await verify_org_access(request.organization_name, current_admin)
        
        result = await OrganizationService.delete_organization(
            organization_name=request.organization_name,
            current_admin=current_admin
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete organization: {str(e)}"
        )

