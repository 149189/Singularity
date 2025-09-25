from datetime import datetime
from ..services.database import get_database
from ..auth.auth_handler import verify_password, get_password_hash
from bson import ObjectId
from typing import Optional

class UserService:
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[dict]:
        db = get_database()
        user = await db.users.find_one({"email": email})
        if user:
            user["id"] = str(user["_id"])
        return user
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[dict]:
        db = get_database()
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            user["id"] = str(user["_id"])
        return user
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[dict]:
        user = await UserService.get_user_by_email(email)
        if not user or not verify_password(password, user["hashed_password"]):
            return None
        return user
    
    @staticmethod
    async def create_user(user_data: dict) -> str:
        db = get_database()
        
        # Initialize game attributes
        user_data.update({
            "level": 1,
            "experience": 0,
            "attributes": {
                "strength": 1,
                "agility": 1,
                "vitality": 1,
                "intelligence": 1
            },
            "inventory": [],
            "active_quests": [],
            "completed_quests": [],
            "created_at": datetime.utcnow()
        })
        
        result = await db.users.insert_one(user_data)
        return str(result.inserted_id)