"""MySQL Repository Implementations - Adapters for data access"""
import mysql.connector
from typing import List, Optional
from ...domain.entities import User
from ...domain.repositories import IUserRepository


class MySQLUserRepository(IUserRepository):
    """MySQL implementation of User repository"""
    
    def __init__(self, db_config: dict):
        self.db_config = db_config
    
    def _get_connection(self):
        """Create database connection"""
        return mysql.connector.connect(**self.db_config)
    
    def _map_db_to_entity(self, row: dict) -> dict:
        """Map database column names to entity attributes"""
        return {
            'id': row.get('id'),
            'username': row.get('id'),  # Use id as username
            'email': row.get('email', ''),
            'password': row.get('password', ''),
            'full_name': row.get('full_name', ''),
            'phone': row.get('phone', ''),
            'address': row.get('address', ''),
            'role': row.get('role', 'user'),
            'created_at': row.get('created_at')
        }
    
    def create(self, user: User) -> Optional[int]:
        """Create new user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Use username or email as id
            user_id = user.username or user.email.split('@')[0]
            
            query = """
                INSERT INTO users (id, email, password, role)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, user.email, user.password, user.role))
            
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if row:
                return User(**self._map_db_to_entity(row))
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username (using id field)"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if row:
                return User(**self._map_db_to_entity(row))
            return None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if row:
                return User(**self._map_db_to_entity(row))
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def update(self, user: User) -> bool:
        """Update user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE users 
                SET email = %s, password = %s, role = %s
                WHERE id = %s
            """
            cursor.execute(query, (user.email, user.password, user.role, user.id))
            
            conn.commit()
            success = cursor.rowcount > 0
            
            cursor.close()
            conn.close()
            
            return success
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def delete(self, user_id: int) -> bool:
        """Delete user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            
            conn.commit()
            success = cursor.rowcount > 0
            
            cursor.close()
            conn.close()
            
            return success
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
