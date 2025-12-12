from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from app.config import settings


class DatabaseManager:
    """Manages MongoDB connections for master database and dynamic organization databases"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.master_db: Optional[AsyncIOMotorDatabase] = None
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
            self.master_db = self.client[settings.master_db_name]
            # Test connection
            await self.client.admin.command('ping')
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Warning: Could not connect to MongoDB: {e}")
            print("Server will start but database operations will fail until MongoDB is available.")
            # Create client anyway so server can start
            self.client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
            self.master_db = self.client[settings.master_db_name]
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")
    
    def get_master_db(self) -> AsyncIOMotorDatabase:
        """Get the master database instance"""
        if not self.master_db:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.master_db
    
    def get_org_database(self, org_collection_name: str) -> AsyncIOMotorDatabase:
        """Get database instance for a specific organization"""
        if not self.client:
            raise RuntimeError("Database not connected. Call connect() first.")
        # Using the same database but different collections
        # In a true multi-tenant setup, you might use separate databases
        return self.client[settings.master_db_name]
    
    async def create_org_collection(self, org_collection_name: str) -> bool:
        """Dynamically create a collection for an organization"""
        try:
            db = self.get_org_database(org_collection_name)
            # Create collection by inserting and deleting a dummy document
            # MongoDB creates collections lazily, so we force creation
            await db[org_collection_name].insert_one({"_initialized": True})
            await db[org_collection_name].delete_one({"_initialized": True})
            return True
        except Exception as e:
            print(f"Error creating collection {org_collection_name}: {e}")
            return False
    
    async def delete_org_collection(self, org_collection_name: str) -> bool:
        """Delete an organization's collection"""
        try:
            db = self.get_org_database(org_collection_name)
            await db[org_collection_name].drop()
            return True
        except Exception as e:
            print(f"Error deleting collection {org_collection_name}: {e}")
            return False
    
    async def collection_exists(self, org_collection_name: str) -> bool:
        """Check if a collection exists"""
        try:
            db = self.get_org_database(org_collection_name)
            collections = await db.list_collection_names()
            return org_collection_name in collections
        except Exception:
            return False
    
    async def copy_collection_data(self, source_collection: str, target_collection: str) -> bool:
        """Copy all data from source collection to target collection"""
        try:
            db = self.get_org_database(source_collection)
            source_coll = db[source_collection]
            target_coll = db[target_collection]
            
            # Get all documents from source
            cursor = source_coll.find({})
            documents = await cursor.to_list(length=None)
            
            if documents:
                await target_coll.insert_many(documents)
            
            return True
        except Exception as e:
            print(f"Error copying collection data: {e}")
            return False


# Global database manager instance
db_manager = DatabaseManager()

