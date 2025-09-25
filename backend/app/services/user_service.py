# backend/app/services/user_service.py
from datetime import datetime
from ..services.database import get_database
from ..auth.auth_handler import verify_password, get_password_hash, validate_password_strength
from bson import ObjectId
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class UserServiceError(Exception):
    """Custom exception for user service errors"""
    pass

class UserService:
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[dict]:
        try:
            db = get_database()
            user = await db.users.find_one({"email": email.lower()})
            if user:
                user["id"] = str(user["_id"])
                del user["_id"]
            return user
        except Exception as e:
            logger.error(f"Error fetching user by email: {e}")
            raise UserServiceError("Database error occurred")
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[dict]:
        try:
            db = get_database()
            user = await db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["id"] = str(user["_id"])
                del user["_id"]
            return user
        except Exception as e:
            logger.error(f"Error fetching user by ID: {e}")
            raise UserServiceError("Database error occurred")
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[dict]:
        try:
            user = await UserService.get_user_by_email(email)
            if not user or not verify_password(password, user["hashed_password"]):
                return None
            return user
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            raise UserServiceError("Authentication error occurred")
    
    @staticmethod
    async def create_user(user_data: dict) -> str:
        try:
            # Validate password strength
            is_valid, message = validate_password_strength(user_data.get("password", ""))
            if not is_valid:
                raise UserServiceError(message)
            
            db = get_database()
            
            # Check if user already exists
            existing_user = await db.users.find_one({"email": user_data["email"].lower()})
            if existing_user:
                raise UserServiceError("Email already registered")
            
            # Hash password and clean up data
            user_data["hashed_password"] = get_password_hash(user_data["password"])
            del user_data["password"]
            user_data["email"] = user_data["email"].lower()
            
            # Initialize game attributes with better defaults
            class_bonuses = {
                "warrior": {"strength": 3, "vitality": 2},
                "mage": {"intelligence": 3, "vitality": 1},
                "rogue": {"agility": 3, "intelligence": 1},
                "cleric": {"vitality": 2, "intelligence": 2, "strength": 1}
            }
            
            bonus = class_bonuses.get(user_data.get("user_class", "warrior"), {"strength": 1})
            base_attributes = {"strength": 1, "agility": 1, "vitality": 1, "intelligence": 1}
            
            for attr, value in bonus.items():
                base_attributes[attr] += value
            
            user_data.update({
                "level": 1,
                "experience": 0,
                "attributes": base_attributes,
                "energy": 100,
                "max_energy": 100,
                "gold": 100,  # Starting gold
                "inventory": [],
                "active_quests": [],
                "completed_quests": [],
                "exercise_logs": [],
                "created_at": datetime.utcnow(),
                "last_login": datetime.utcnow(),
                "last_energy_update": datetime.utcnow()
            })
            
            result = await db.users.insert_one(user_data)
            return str(result.inserted_id)
            
        except UserServiceError:
            raise
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise UserServiceError("User creation failed")

    @staticmethod
    async def update_user_stats(user_id: str, experience_gained: int, attributes_gained: dict) -> bool:
        """Update user experience and attributes"""
        try:
            db = get_database()
            
            # Calculate level progression
            user = await UserService.get_user_by_id(user_id)
            if not user:
                return False
            
            new_experience = user["experience"] + experience_gained
            new_level = user["level"]
            
            # Simple level calculation: 100 XP per level with scaling
            while new_experience >= (new_level * 100):
                new_experience -= (new_level * 100)
                new_level += 1
            
            # Update attributes
            current_attributes = user.get("attributes", {})
            for attr, gain in attributes_gained.items():
                current_attributes[attr] = current_attributes.get(attr, 1) + gain
            
            # Update user
            update_result = await db.users.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "level": new_level,
                        "experience": new_experience,
                        "attributes": current_attributes,
                        "last_activity": datetime.utcnow()
                    }
                }
            )
            
            return update_result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating user stats: {e}")
            return False