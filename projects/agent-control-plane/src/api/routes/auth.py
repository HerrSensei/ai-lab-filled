#!/usr/bin/env python3
"""
Authentication API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.token_manager import TokenManager
from src.auth.user_manager import UserManager

router = APIRouter()
security = HTTPBearer()
user_manager = UserManager()
token_manager = TokenManager()


@router.post("/login")
async def login(username: str, password: str):
    """Login and get access token"""
    try:
        await user_manager.initialize()

        # Authenticate user
        user = await user_manager.authenticate_user(username, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Create tokens
        access_token = token_manager.create_access_token(
            {"sub": username, "role": user.get("role", "user")}
        )
        refresh_token = token_manager.create_refresh_token({"sub": username})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/refresh")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh access token"""
    try:
        # Verify refresh token
        token_data = token_manager.verify_token(credentials.credentials)
        if not token_data:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Create new access token
        access_token = token_manager.create_access_token({"sub": token_data.get("sub")})

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout and blacklist token"""
    try:
        token_manager.blacklist_token(credentials.credentials)
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Get current user information"""
    try:
        token_data = token_manager.verify_token(credentials.credentials)
        if not token_data:
            raise HTTPException(status_code=401, detail="Invalid token")

        await user_manager.initialize()
        user = await user_manager.get_user(token_data.get("sub"))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
