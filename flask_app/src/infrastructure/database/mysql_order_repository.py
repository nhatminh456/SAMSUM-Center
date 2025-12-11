"""MySQL Order Repository Implementation"""
import mysql.connector
from typing import List, Optional
from ...domain.entities import Order, OrderItem, OrderStatus
from ...domain.repositories import IOrderRepository


class MySQLOrderRepository(IOrderRepository):
    """MySQL implementation of Order repository"""
    
    def __init__(self, db_config: dict):
        self.db_config = db_config
    
    def _get_connection(self):
        """Create database connection"""
        return mysql.connector.connect(**self.db_config)
    
    def create(self, order: Order) -> Optional[str]:
        """Create new order with items"""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Insert order
            order_query = """
                INSERT INTO orders (id, user_id, customer_name, customer_phone, 
                                   customer_address, payment_method, total_amount, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(order_query, (
                order.id, order.user_id, order.customer_name, order.customer_phone,
                order.customer_address, order.payment_method, order.total_amount,
                order.status.value
            ))
            
            # Insert order items
            item_query = """
                INSERT INTO order_items (order_id, product_id, product_name, 
                                        product_price, quantity, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            for item in order.items:
                cursor.execute(item_query, (
                    order.id, item.product_id, item.product_name,
                    item.product_price, item.quantity, item.subtotal
                ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return order.id
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            print(f"Error creating order: {e}")
            return None
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by ID with items"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get order
            order_query = "SELECT * FROM orders WHERE id = %s"
            cursor.execute(order_query, (order_id,))
            order_row = cursor.fetchone()
            
            if not order_row:
                cursor.close()
                conn.close()
                return None
            
            # Get order items
            items_query = "SELECT * FROM order_items WHERE order_id = %s"
            cursor.execute(items_query, (order_id,))
            items_rows = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            # Create Order entity
            order = Order(
                id=order_row['id'],
                user_id=order_row['user_id'],
                customer_name=order_row['customer_name'],
                customer_phone=order_row['customer_phone'],
                customer_address=order_row['customer_address'],
                payment_method=order_row['payment_method'],
                total_amount=order_row['total_amount'],
                status=OrderStatus.from_string(order_row['status']),
                created_at=order_row['created_at']
            )
            
            # Add items
            for item_row in items_rows:
                item = OrderItem(**item_row)
                order.items.append(item)
            
            return order
        except Exception as e:
            print(f"Error getting order: {e}")
            return None
    
    def get_by_user(self, user_id: int) -> List[Order]:
        """Get all orders by user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC"
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            orders = []
            for row in rows:
                order = Order(
                    id=row['id'],
                    user_id=row['user_id'],
                    customer_name=row['customer_name'],
                    customer_phone=row['customer_phone'],
                    customer_address=row['customer_address'],
                    payment_method=row['payment_method'],
                    total_amount=row['total_amount'],
                    status=OrderStatus.from_string(row['status']),
                    created_at=row['created_at']
                )
                orders.append(order)
            
            return orders
        except Exception as e:
            print(f"Error getting user orders: {e}")
            return []
    
    def get_all(self) -> List[Order]:
        """Get all orders"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM orders ORDER BY created_at DESC"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            orders = []
            for row in rows:
                order = Order(
                    id=row['id'],
                    user_id=row['user_id'],
                    customer_name=row['customer_name'],
                    customer_phone=row['customer_phone'],
                    customer_address=row['customer_address'],
                    payment_method=row['payment_method'],
                    total_amount=row['total_amount'],
                    status=OrderStatus.from_string(row['status']),
                    created_at=row['created_at']
                )
                orders.append(order)
            
            return orders
        except Exception as e:
            print(f"Error getting all orders: {e}")
            return []
    
    def update_status(self, order_id: str, status: str) -> bool:
        """Update order status"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = "UPDATE orders SET status = %s WHERE id = %s"
            cursor.execute(query, (status, order_id))
            
            conn.commit()
            success = cursor.rowcount > 0
            
            cursor.close()
            conn.close()
            
            return success
        except Exception as e:
            print(f"Error updating order status: {e}")
            return False
