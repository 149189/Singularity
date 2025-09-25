from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth
from .services.database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="Singularity API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

@app.on_event("startup")
async def startup_event():
    try:
        await connect_to_mongo()
    except Exception as e:
        print(f"⚠️  Starting without database connection: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to Singularity API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Singularity API is running"}