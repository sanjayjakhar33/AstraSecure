"""
Authentication endpoints
"""
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.services import user_service

router = APIRouter()


@router.post("/login", response_model=schemas.UserToken)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_service.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user
    }


@router.post("/register", response_model=schemas.User)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate
) -> Any:
    """
    Register new user
    """
    user = user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists"
        )
    
    user = user_service.create(db, obj_in=user_in)
    return user


@router.post("/password-reset", response_model=dict)
def reset_password(
    email: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Password reset request
    """
    user = user_service.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User with this email does not exist"
        )
    
    # In a real application, you would send an email here
    reset_token = security.create_password_reset_token(email)
    
    return {
        "message": "Password reset token generated",
        "reset_token": reset_token  # In production, this would be sent via email
    }


@router.post("/password-reset-confirm", response_model=dict)
def reset_password_confirm(
    *,
    db: Session = Depends(deps.get_db),
    reset_data: schemas.PasswordResetConfirm
) -> Any:
    """
    Confirm password reset
    """
    email = security.verify_token(reset_data.token)
    if not email:
        raise HTTPException(
            status_code=400,
            detail="Invalid token"
        )
    
    user = user_service.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    hashed_password = security.get_password_hash(reset_data.new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    
    return {"message": "Password updated successfully"}


@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    """
    Get current user
    """
    return current_user