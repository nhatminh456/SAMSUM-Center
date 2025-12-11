"""MySQL Category Repository Implementation"""
import mysql.connector
from typing import List, Optional
from ...domain.entities import Category
from ...domain.repositories import ICategoryRepository


class MySQLCategoryRepository(ICategoryRepository):
    """MySQL implementation of Category repository"""
    
    def __init__(self, db_config: dict):
        self.db_config = db_config
    
    def _get_connection(self):
        """Create database connection"""
        return mysql.connector.connect(**self.db_config)
    
    def _map_db_to_entity(self, row: dict) -> dict:
        """Map database column names to entity attributes"""
        return {
            'id': row.get('id'),
            'name': row.get('tenDM', ''),
            'description': row.get('description', '')
        }
    
    def create(self, category: Category) -> Optional[int]:
        """Create new category"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = "INSERT INTO categories (tenDM) VALUES (%s)"
            cursor.execute(query, (category.name,))
            
            conn.commit()
            category_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return category_id
        except Exception as e:
            print(f"Error creating category: {e}")
            return None
    
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM categories WHERE id = %s"
            cursor.execute(query, (category_id,))
            row = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if row:
                return Category(**self._map_db_to_entity(row))
            return None
        except Exception as e:
            print(f"Error getting category: {e}")
            return None
    
    def get_all(self) -> List[Category]:
        """Get all categories"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM categories ORDER BY tenDM"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [Category(**self._map_db_to_entity(row)) for row in rows]
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def update(self, category: Category) -> bool:
        """Update category"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = "UPDATE categories SET tenDM = %s WHERE id = %s"
            cursor.execute(query, (category.name, category.id))
            
            conn.commit()
            success = cursor.rowcount > 0
            
            cursor.close()
            conn.close()
            
            return success
        except Exception as e:
            print(f"Error updating category: {e}")
            return False
    
    def delete(self, category_id: int) -> bool:
        """Delete category"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM categories WHERE id = %s"
            cursor.execute(query, (category_id,))
            
            conn.commit()
            success = cursor.rowcount > 0
            
            cursor.close()
            conn.close()
            
            return success
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False
