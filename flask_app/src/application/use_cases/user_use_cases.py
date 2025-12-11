"""User Use Cases - Application Business Logic"""
from typing import Optional
from ...domain.entities import User
from ...domain.repositories import IUserRepository
import hashlib


class RegisterUserUseCase:
    """Use case for user registration"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(self, user: User) -> tuple[bool, str, Optional[int]]:
        """
        Execute user registration
        Returns: (success, message, user_id)
        """
        # Validate user data
        is_valid, error_msg = user.is_valid_for_registration()
        if not is_valid:
            return False, error_msg, None
        
        # Check if username exists
        existing_user = self.user_repository.get_by_username(user.username)
        if existing_user:
            return False, "Username đã tồn tại", None
        
        # Check if email exists
        existing_email = self.user_repository.get_by_email(user.email)
        if existing_email:
            return False, "Email đã được sử dụng", None
        
        # Hash password (TODO: Use bcrypt in production)
        # user.password = hashlib.sha256(user.password.encode()).hexdigest()
        
        # Create user
        user_id = self.user_repository.create(user)
        if user_id:
            return True, "Đăng ký thành công", user_id
        
        return False, "Đã xảy ra lỗi khi tạo tài khoản", None


class LoginUserUseCase:
    """Use case for user login"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(self, username: str, password: str) -> tuple[bool, str, Optional[User]]:
        """
        Execute user login
        Returns: (success, message, user)
        """
        if not username or not password:
            return False, "Username và password không được để trống", None
        
        # Try to get user by username (id field) first
        user = self.user_repository.get_by_username(username)
        
        # If not found, try by email
        if not user and '@' in username:
            user = self.user_repository.get_by_email(username)
        
        if not user:
            return False, "Username hoặc password không đúng", None
        
        # Verify password (direct comparison - no hashing)
        if user.password != password:
            return False, "Username hoặc password không đúng", None
        
        return True, "Đăng nhập thành công", user


class GetUserProfileUseCase:
    """Use case for getting user profile"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: int) -> Optional[User]:
        """Get user profile by ID"""
        return self.user_repository.get_by_id(user_id)


class UpdateUserProfileUseCase:
    """Use case for updating user profile"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(self, user: User) -> tuple[bool, str]:
        """
        Update user profile
        Returns: (success, message)
        """
        if not user.id:
            return False, "User ID không hợp lệ"
        
        success = self.user_repository.update(user)
        if success:
            return True, "Cập nhật thông tin thành công"
        
        return False, "Đã xảy ra lỗi khi cập nhật"
