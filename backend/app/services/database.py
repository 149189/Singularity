from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

mongodb = MongoDB()

async def connect_to_mongo():
    try:
        # Simple local connection
        mongodb.client = AsyncIOMotorClient(
            os.getenv("MONGODB_URL", "mongodb://localhost:27017"),
            serverSelectionTimeoutMS=3000
        )
        
        # Test connection
        await mongodb.client.admin.command('ping')
        
        mongodb.database = mongodb.client[os.getenv("DATABASE_NAME", "singularity_local")]
        print(f"✅ Connected to MongoDB: {os.getenv('DATABASE_NAME', 'singularity_local')}")
        
        # Create indexes for better performance
        await create_indexes()
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        traceback.print_exc() 
        print("📝 Make sure MongoDB is running on localhost:27017")
        # Don't raise exception - let the app start without DB for testing
        print("⚠️  App will continue without database connection")

async def create_indexes():
    """Create database indexes for better performance"""
    try:
        db = mongodb.database
        
        # User indexes
        await db.users.create_index("email", unique=True)
        await db.users.create_index("username")
        
        # Exercise log indexes
        await db.exercise_logs.create_index("user_id")
        await db.exercise_logs.create_index("completed_at")
        
        print("📊 Database indexes created")
        
    except Exception as e:
        print(f"⚠️  Index creation failed: {e}")

async def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()
        print("🔌 Disconnected from MongoDB")

def get_database():
    if mongodb.database is None:
        raise Exception("Database not connected. Please start MongoDB and restart the server.")
    return mongodb.database