"""MySQL Product Repository Implementation"""
import mysql.connector
from typing import List, Optional
from ...domain.entities import Product
from ...domain.repositories import IProductRepository


class MySQLProductRepository(IProductRepository):
    """MySQL implementation of Product repository"""
    
    def __init__(self, db_config: dict):
        self.db_config = db_config
    
    def _get_connection(self):
        """Create database connection"""
        return mysql.connector.connect(**self.db_config)
    
    def _map_db_to_entity(self, row: dict) -> dict:
        """Map database column names to entity attributes"""
        return {
            'id': row.get('id'),
            'name': row.get('tenSP'),
            'description': row.get('mota', ''),
            'price': float(row.get('gia', 0)),
            'category_id': row.get('categoryID'),
            'category_name': row.get('category_name') or row.get('tenDM'),
            'image_url': row.get('image', ''),
            'stock_quantity': row.get('stock_quantity', 100),
            'bestSeller': row.get('bestSeller', 0),
            'created_at': row.get('created_at')
        }
    
    def create(self, product: Product) -> Optional[int]:
        """Create new product"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO products (tenSP, mota, gia, categoryID, image)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                product.name, product.description, product.price,
                product.category_id, product.image_url
            ))
            
            conn.commit()
            product_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return product_id
        except Exception as e:
            print(f"Error creating product: {e}")
            return None
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT p.*, c.tenDM as category_name
                FROM products p
                LEFT JOIN categories c ON p.categoryID = c.id
                WHERE p.id = %s
            """
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if row:
                return Product(**self._map_db_to_entity(row))
            return None
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
    
    def get_all(self) -> List[Product]:
        """Get all products"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT p.*, c.tenDM as category_name
                FROM products p
                LEFT JOIN categories c ON p.categoryID = c.id
                ORDER BY p.id DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [Product(**self._map_db_to_entity(row)) for row in rows]
        except Exception as e:
            print(f"Error getting products: {e}")
            return []
    
    def get_by_category(self, category_id: int) -> List[Product]:
        """Get products by category"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT p.*, c.tenDM as category_name
                FROM products p
                LEFT JOIN categories c ON p.categoryID = c.id
                WHERE p.categoryID = %s
                ORDER BY p.id DESC
            """
            cursor.execute(query, (category_id,))
            rows = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [Product(**self._map_db_to_entity(row)) for row in rows]
        except Exception as e:
            print(f"Error getting products by category: {e}")
            return []
    
    def search(self, keyword: str) -> List[Product]:
        """Search products by keyword"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT p.*, c.tenDM as category_name
                FROM products p
                LEFT JOIN categories c ON p.categoryID = c.id
                WHERE p.tenSP LIKE %s OR p.mota LIKE %s
                ORDER BY p.id DESC
            """
            search_term = f"%{keyword}%"
            cursor.execute(query, (search_term, search_term))
            rows = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [Product(**self._map_db_to_entity(row)) for row in rows]
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def update(self, product: Product) -> bool:
        """Update product"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE products
                SET tenSP = %s, mota = %s, gia = %s, categoryID = %s, image = %s
                WHERE id = %s
            """
            cursor.execute(query, (
                product.name, product.description, product.price, product.category_id,
                product.image_url, product.id
            ))
            
            conn.commit()
            success = cursor.rowcount > 0
            
            cursor.close()
            conn.close()
            
            return success
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
    
    def delete(self, product_id: int) -> bool:
        """Delete product"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM products WHERE id = %s"
            cursor.execute(query, (product_id,))
            
            conn.commit()
            success = cursor.rowcount > 0
            
            cursor.close()
            conn.close()
            
            return success
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Update product stock quantity"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = "UPDATE products SET stock_quantity = %s WHERE id = %s"
            cursor.execute(query, (quantity, product_id))
            
            conn.commit()
            success = cursor.rowcount > 0
            
            cursor.close()
            conn.close()
            
            return success
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False
