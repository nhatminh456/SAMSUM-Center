"""User Entity - Domain Model"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """User domain entity representing a customer or admin"""
    
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password: str = ""
    full_name: str = ""
    phone: str = ""
    address: str = ""
    role: str = "user"  # user or admin
    created_at: Optional[datetime] = None
    
    def is_admin(self) -> bool:
        """Check if user has admin role"""
        return self.role == "admin"
    
    def is_valid_for_registration(self) -> tuple[bool, str]:
        """Validate user data for registration"""
        if not self.username or len(self.username) < 3:
            return False, "Username phải có ít nhất 3 ký tự"
        
        if not self.email or "@" not in self.email:
            return False, "Email không hợp lệ"
        
        if not self.password or len(self.password) < 6:
            return False, "Password phải có ít nhất 6 ký tự"
        
        if not self.full_name:
            return False, "Họ tên không được để trống"
        
        return True, ""
    
    def to_dict(self) -> dict:
        """Convert entity to dictionary (exclude password)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'role': self.role,
            'created_at': self.created_at
        }
