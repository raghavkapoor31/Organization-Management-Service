from typing import Optional
from bson import ObjectId
from app.database import db_manager
from app.models.organization import Organization, AdminUser
from app.auth.password import hash_password, verify_password
from app.auth.jwt_handler import JWTHandler
from fastapi import HTTPException, status
import re


class OrganizationService:
    """Service class for organization management operations"""
    
    @staticmethod
    def sanitize_org_name(organization_name: str) -> str:
        """Convert organization name to valid collection name"""
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', organization_name)
        # Remove consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        # Ensure it starts with a letter or number
        if not sanitized or not (sanitized[0].isalnum()):
            sanitized = 'org_' + sanitized if sanitized else 'org_default'
        return f"org_{sanitized.lower()}"
    
    @staticmethod
    async def create_organization(
        organization_name: str,
        email: str,
        password: str
    ) -> dict:
        """Create a new organization with admin user"""
        master_db = db_manager.get_master_db()
        orgs_collection = master_db["organizations"]
        admins_collection = master_db["admin_users"]
        
        # Check if organization already exists
        existing_org = await orgs_collection.find_one({
            "organization_name": organization_name
        })
        if existing_org:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization name already exists"
            )
        
        # Check if email already exists
        existing_admin = await admins_collection.find_one({"email": email})
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create organization collection name
        org_collection_name = OrganizationService.sanitize_org_name(organization_name)
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Create admin user
        admin_user = AdminUser(
            email=email,
            hashed_password=hashed_password,
            organization_name=organization_name
        )
        admin_result = await admins_collection.insert_one(admin_user.to_dict())
        admin_user_id = str(admin_result.inserted_id)
        
        # Create organization
        organization = Organization(
            organization_name=organization_name,
            org_collection_name=org_collection_name,
            admin_user_id=admin_user_id
        )
        org_result = await orgs_collection.insert_one(organization.to_dict())
        
        # Create organization's collection
        collection_created = await db_manager.create_org_collection(org_collection_name)
        if not collection_created:
            # Rollback: delete organization and admin if collection creation fails
            await orgs_collection.delete_one({"_id": org_result.inserted_id})
            await admins_collection.delete_one({"_id": admin_result.inserted_id})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create organization collection"
            )
        
        return {
            "organization_name": organization.organization_name,
            "org_collection_name": organization.org_collection_name,
            "admin_user_id": admin_user_id,
            "created_at": organization.created_at,
            "updated_at": organization.updated_at
        }
    
    @staticmethod
    async def get_organization(organization_name: str) -> dict:
        """Get organization details by name"""
        master_db = db_manager.get_master_db()
        orgs_collection = master_db["organizations"]
        
        org_data = await orgs_collection.find_one({
            "organization_name": organization_name
        })
        
        if not org_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Convert ObjectId to string
        org_data["admin_user_id"] = str(org_data["admin_user_id"])
        org_data["_id"] = str(org_data["_id"])
        
        return org_data
    
    @staticmethod
    async def update_organization(
        organization_name: str,
        new_email: str,
        new_password: str,
        current_admin: dict,
        new_organization_name: Optional[str] = None
    ) -> dict:
        """Update organization (rename and migrate data if new name provided)"""
        master_db = db_manager.get_master_db()
        orgs_collection = master_db["organizations"]
        admins_collection = master_db["admin_users"]
        
        # Get existing organization
        existing_org = await orgs_collection.find_one({
            "organization_name": organization_name
        })
        
        if not existing_org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Verify admin has access
        if current_admin["organization_name"] != organization_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this organization"
            )
        
        from datetime import datetime
        
        # Handle organization name change if provided
        final_org_name = organization_name
        old_collection_name = existing_org["org_collection_name"]
        
        if new_organization_name and new_organization_name != organization_name:
            # Validate that new organization name does not already exist
            existing_new_org = await orgs_collection.find_one({
                "organization_name": new_organization_name
            })
            if existing_new_org:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New organization name already exists"
                )
            
            # Create new collection name
            new_collection_name = OrganizationService.sanitize_org_name(new_organization_name)
            
            # Check if new collection already exists
            if await db_manager.collection_exists(new_collection_name):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Collection for new organization name already exists"
                )
            
            # Create new collection
            collection_created = await db_manager.create_org_collection(new_collection_name)
            if not collection_created:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create new organization collection"
                )
            
            # Copy data from old collection to new collection
            if await db_manager.collection_exists(old_collection_name):
                data_copied = await db_manager.copy_collection_data(
                    old_collection_name,
                    new_collection_name
                )
                if not data_copied:
                    # Rollback: delete new collection
                    await db_manager.delete_org_collection(new_collection_name)
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to migrate data to new collection"
                    )
            
            # Update organization metadata with new name and collection
            final_org_name = new_organization_name
            await orgs_collection.update_one(
                {"organization_name": organization_name},
                {
                    "$set": {
                        "organization_name": new_organization_name,
                        "org_collection_name": new_collection_name,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            # Update admin user with new organization name
            admin_id = ObjectId(existing_org["admin_user_id"])
            await admins_collection.update_one(
                {"_id": admin_id},
                {
                    "$set": {
                        "organization_name": new_organization_name
                    }
                }
            )
            
            # Delete old collection after successful migration
            await db_manager.delete_org_collection(old_collection_name)
        
        # Update admin user credentials
        admin_id = ObjectId(existing_org["admin_user_id"])
        hashed_password = hash_password(new_password)
        
        await admins_collection.update_one(
            {"_id": admin_id},
            {
                "$set": {
                    "email": new_email,
                    "hashed_password": hashed_password
                }
            }
        )
        
        # Update organization updated_at if name wasn't changed
        if not new_organization_name or new_organization_name == organization_name:
            await orgs_collection.update_one(
                {"organization_name": final_org_name},
                {
                    "$set": {
                        "updated_at": datetime.utcnow()
                    }
                }
            )
        
        # Get updated organization
        updated_org = await orgs_collection.find_one({
            "organization_name": final_org_name
        })
        
        updated_org["admin_user_id"] = str(updated_org["admin_user_id"])
        updated_org["_id"] = str(updated_org["_id"])
        
        return updated_org
    
    @staticmethod
    async def delete_organization(
        organization_name: str,
        current_admin: dict
    ) -> dict:
        """Delete organization and its collection"""
        master_db = db_manager.get_master_db()
        orgs_collection = master_db["organizations"]
        admins_collection = master_db["admin_users"]
        
        # Get organization
        org_data = await orgs_collection.find_one({
            "organization_name": organization_name
        })
        
        if not org_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        # Verify admin has access
        if current_admin["organization_name"] != organization_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this organization"
            )
        
        # Delete organization collection
        org_collection_name = org_data["org_collection_name"]
        await db_manager.delete_org_collection(org_collection_name)
        
        # Delete admin user
        admin_id = ObjectId(org_data["admin_user_id"])
        await admins_collection.delete_one({"_id": admin_id})
        
        # Delete organization
        await orgs_collection.delete_one({"organization_name": organization_name})
        
        return {
            "message": "Organization deleted successfully",
            "organization_name": organization_name
        }
    
    @staticmethod
    async def authenticate_admin(email: str, password: str) -> dict:
        """Authenticate admin and return JWT token"""
        master_db = db_manager.get_master_db()
        admins_collection = master_db["admin_users"]
        
        # Find admin by email
        admin_data = await admins_collection.find_one({"email": email})
        
        if not admin_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(password, admin_data["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Create JWT token
        admin_id = str(admin_data["_id"])
        organization_name = admin_data["organization_name"]
        token = JWTHandler.create_admin_token(admin_id, organization_name)
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "organization_name": organization_name,
            "admin_id": admin_id
        }

