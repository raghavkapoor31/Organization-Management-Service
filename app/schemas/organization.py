from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class OrganizationCreateRequest(BaseModel):
    organization_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)


class OrganizationGetRequest(BaseModel):
    organization_name: str = Field(..., min_length=1)


class OrganizationUpdateRequest(BaseModel):
    organization_name: str = Field(..., min_length=1)  # Current organization name (identifier)
    new_organization_name: Optional[str] = Field(None, min_length=1, max_length=100)  # Optional new name
    email: EmailStr
    password: str = Field(..., min_length=8)


class OrganizationDeleteRequest(BaseModel):
    organization_name: str = Field(..., min_length=1)


class OrganizationResponse(BaseModel):
    organization_name: str
    org_collection_name: str
    admin_user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    organization_name: str
    admin_id: str

