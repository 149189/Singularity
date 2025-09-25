# backend/app/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..models.user import UserCreate, UserLogin, UserResponse
from ..services.user_service import UserService, UserServiceError
from ..auth.auth_handler import (
    verify_token, create_access_token, create_refresh_token, validate_password_strength
)
from datetime import timedelta
import time
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

# Simple rate limiting (in production, use Redis)
request_counts = {}
RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_WINDOW = 300  # 5 minutes

def rate_limit_check(request: Request):
    client_ip = request.client.host
    current_time = time.time()
    
    if client_ip not in request_counts:
        request_counts[client_ip] = []
    
    # Clean old requests
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip]
        if current_time - req_time < RATE_LIMIT_WINDOW
    ]
    
    if len(request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )
    
    request_counts[client_ip].append(current_time)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await UserService.get_user_by_email(payload.get("email"))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except UserServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register", response_model=dict)
async def register(user_data: UserCreate, request: Request):
    try:
        rate_limit_check(request)
        
        # Validate password strength
        is_valid, message = validate_password_strength(user_data.password)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        user_dict = user_data.dict()
        user_id = await UserService.create_user(user_dict)
        user = await UserService.get_user_by_id(user_id)
        
        # Create tokens
        access_token = create_access_token(data={"email": user["email"]})
        refresh_token = create_refresh_token(data={"email": user["email"]})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": UserResponse(**user)
        }
        
    except UserServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login")
async def login(login_data: UserLogin, request: Request):
    try:
        rate_limit_check(request)
        
        user = await UserService.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Update last login
        db = get_database()
        await db.users.update_one(
            {"_id": ObjectId(user["id"])},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        access_token = create_access_token(data={"email": user["email"]})
        refresh_token = create_refresh_token(data={"email": user["email"]})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": UserResponse(**user)
        }
        
    except UserServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = verify_token(refresh_token, "refresh")
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # Create new access token
        access_token = create_access_token(data={"email": payload.get("email")})
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(status_code=401, detail="Token refresh failed")

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return UserResponse(**current_user)