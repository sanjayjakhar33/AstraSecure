"""
User service layer
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class UserService:
    """User service for CRUD operations"""
    
    def get(self, db: Session, id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    def get_by_api_key(self, db: Session, api_key: str) -> Optional[User]:
        """Get user by API key"""
        return db.query(User).filter(User.api_key == api_key).first()
    
    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        company_id: Optional[int] = None
    ) -> List[User]:
        """Get multiple users with pagination"""
        query = db.query(User)
        if company_id is not None:
            query = query.filter(User.company_id == company_id)
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create new user"""
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            email=obj_in.email,
            hashed_password=hashed_password,
            full_name=obj_in.full_name,
            phone=obj_in.phone,
            job_title=obj_in.job_title,
            role=obj_in.role,
            is_active=obj_in.is_active,
            company_id=obj_in.company_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """Update user"""
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: int) -> User:
        """Delete user"""
        obj = db.query(User).get(id)
        db.delete(obj)
        db.commit()
        return obj
    
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.add(user)
        db.commit()
        
        return user
    
    def is_active(self, user: User) -> bool:
        """Check if user is active"""
        return user.is_active
    
    def is_superuser(self, user: User) -> bool:
        """Check if user is superuser"""
        return user.is_superuser


# Create service instance
user_service = UserService()