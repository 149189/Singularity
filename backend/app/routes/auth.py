from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..models.user import UserCreate, UserLogin, UserResponse
from ..services.user_service import UserService
from ..auth.auth_handler import verify_token, get_password_hash, create_access_token

router = APIRouter()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await UserService.get_user_by_email(payload.get("email"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    existing_user = await UserService.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user_data.dict()
    user_dict["hashed_password"] = get_password_hash(user_data.password)
    del user_dict["password"]
    
    user_id = await UserService.create_user(user_dict)
    user = await UserService.get_user_by_id(user_id)
    
    # Create token for immediate login after registration
    access_token = create_access_token(data={"email": user["email"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**user)
    }

@router.post("/login")
async def login(login_data: UserLogin):
    user = await UserService.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"email": user["email"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**user)
    }