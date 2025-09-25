from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth  #, exercises, game  # Comment out non-existent routes for now
from .services.database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="Singularity API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (only auth for now)
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(exercises.router, prefix="/api/exercises", tags=["Exercises"])
# app.include_router(game.router, prefix="/api/game", tags=["Game"])

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to Singularity API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Singularity API is running"}