# debug_test.py - Run this in your backend directory to test
import asyncio
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.services.database import connect_to_mongo, get_database
from app.services.user_service import UserService

async def test_user_creation():
    print("🔧 Testing user creation...")
    
    try:
        # Connect to database
        await connect_to_mongo()
        print("✅ Database connected")
        
        # Test data
        test_user = {
            "username": "testuser123",
            "email": "test123@example.com",
            "password": "TestPassword123",
            "full_name": "Test User",
            "user_class": "warrior"
        }
        
        print(f"📝 Creating user: {test_user['username']}")
        
        # Try to create user
        user_id = await UserService.create_user(test_user)
        print(f"✅ User created successfully with ID: {user_id}")
        
        # Fetch the created user
        user = await UserService.get_user_by_id(user_id)
        print(f"✅ User fetched: {user['username']} - {user['email']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_user_creation())