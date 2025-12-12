from typing import Optional
from datetime import datetime
from bson import ObjectId


class Organization:
    """Organization model for master database"""
    
    def __init__(
        self,
        organization_name: str,
        org_collection_name: str,
        admin_user_id: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id or ObjectId()
        self.organization_name = organization_name
        self.org_collection_name = org_collection_name
        self.admin_user_id = admin_user_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB storage"""
        return {
            "_id": self._id,
            "organization_name": self.organization_name,
            "org_collection_name": self.org_collection_name,
            "admin_user_id": self.admin_user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Organization":
        """Create Organization instance from dictionary"""
        return cls(
            _id=data.get("_id"),
            organization_name=data["organization_name"],
            org_collection_name=data["org_collection_name"],
            admin_user_id=data["admin_user_id"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


class AdminUser:
    """Admin user model for master database"""
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        organization_name: str,
        created_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id or ObjectId()
        self.email = email
        self.hashed_password = hashed_password
        self.organization_name = organization_name
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB storage"""
        return {
            "_id": self._id,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "organization_name": self.organization_name,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AdminUser":
        """Create AdminUser instance from dictionary"""
        return cls(
            _id=data.get("_id"),
            email=data["email"],
            hashed_password=data["hashed_password"],
            organization_name=data["organization_name"],
            created_at=data.get("created_at")
        )

