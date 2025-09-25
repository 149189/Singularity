from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routes import auth
from .services.database import connect_to_mongo, close_mongo_connection
import logging
import traceback

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Singularity API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    logger.error(f"Request: {request.method} {request.url}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error occurred",
            "error": str(exc)
        }
    )

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

@app.on_event("startup")
async def startup_event():
    try:
        await connect_to_mongo()
        logger.info("🚀 Singularity API started successfully")
    except Exception as e:
        logger.error(f"⚠️  Starting without database connection: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    logger.info("🛑 Singularity API shutting down")

@app.get("/")
async def root():
    return {"message": "Welcome to Singularity API"}

@app.get("/api/health")
async def health_check():
    try:
        # Test database connection
        from .services.database import get_database
        db = get_database()
        await db.command("ping")
        db_status = "connected"
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        db_status = "disconnected"
    
    return {
        "status": "healthy", 
        "message": "Singularity API is running",
        "database": db_status
    }