"""
User management endpoints
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.services import user_service

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_superuser)
) -> Any:
    """
    Retrieve users (superuser only)
    """
    users = user_service.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get current user
    """
    return current_user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    current_user: schemas.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Update current user
    """
    user = user_service.get(db, id=current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = user_service.update(db, db_obj=user, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: schemas.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get a specific user by ID
    """
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Users can only see their own data unless they're superuser or company admin
    if user.id != current_user.id and not current_user.is_superuser:
        from app.models.user import UserRole
        if current_user.role != UserRole.COMPANY_ADMIN or user.company_id != current_user.company_id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: schemas.User = Depends(deps.get_current_superuser)
) -> Any:
    """
    Update a user (superuser only)
    """
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = user_service.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: schemas.User = Depends(deps.get_current_superuser)
) -> Any:
    """
    Delete a user (superuser only)
    """
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = user_service.delete(db, id=user_id)
    return user