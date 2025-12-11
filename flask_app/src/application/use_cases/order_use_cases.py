"""Order Use Cases - Application Business Logic"""
from typing import List, Optional
from ...domain.entities import Order, OrderItem, OrderStatus
from ...domain.repositories import IOrderRepository, IProductRepository
import time
import uuid


class CreateOrderUseCase:
    """Use case for creating order"""
    
    def __init__(self, order_repository: IOrderRepository, product_repository: IProductRepository):
        self.order_repository = order_repository
        self.product_repository = product_repository
    
    def execute(self, order: Order) -> tuple[bool, str, Optional[str]]:
        """
        Create new order
        Returns: (success, message, order_id)
        """
        # Validate order
        is_valid, error_msg = order.is_valid()
        if not is_valid:
            return False, error_msg, None
        
        # Validate stock for all items
        for item in order.items:
            product = self.product_repository.get_by_id(item.product_id)
            if not product:
                return False, f"Sản phẩm {item.product_name} không tồn tại", None
            
            can_buy, error_msg = product.can_purchase(item.quantity)
            if not can_buy:
                return False, f"{item.product_name}: {error_msg}", None
        
        # Generate order ID
        timestamp = time.strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:4]
        order.id = f"ORD{timestamp}{unique_id.upper()}"
        
        # Calculate total
        order.calculate_total()
        
        # Create order
        order_id = self.order_repository.create(order)
        if order_id:
            # Update stock for all items
            for item in order.items:
                product = self.product_repository.get_by_id(item.product_id)
                new_stock = product.stock_quantity - item.quantity
                self.product_repository.update_stock(item.product_id, new_stock)
            
            return True, "Đặt hàng thành công", order_id
        
        return False, "Đã xảy ra lỗi khi tạo đơn hàng", None


class GetUserOrdersUseCase:
    """Use case for getting user's orders"""
    
    def __init__(self, order_repository: IOrderRepository):
        self.order_repository = order_repository
    
    def execute(self, user_id: int) -> List[Order]:
        """Get all orders by user"""
        return self.order_repository.get_by_user(user_id)


class GetOrderByIdUseCase:
    """Use case for getting order by ID"""
    
    def __init__(self, order_repository: IOrderRepository):
        self.order_repository = order_repository
    
    def execute(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        return self.order_repository.get_by_id(order_id)


class GetAllOrdersUseCase:
    """Use case for getting all orders (admin)"""
    
    def __init__(self, order_repository: IOrderRepository):
        self.order_repository = order_repository
    
    def execute(self) -> List[Order]:
        """Get all orders"""
        return self.order_repository.get_all()


class UpdateOrderStatusUseCase:
    """Use case for updating order status (admin)"""
    
    def __init__(self, order_repository: IOrderRepository):
        self.order_repository = order_repository
    
    def execute(self, order_id: str, new_status: str) -> tuple[bool, str]:
        """
        Update order status
        Returns: (success, message)
        """
        # Get current order
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return False, "Đơn hàng không tồn tại"
        
        # Parse new status
        try:
            status = OrderStatus.from_string(new_status)
        except:
            return False, "Trạng thái không hợp lệ"
        
        # Check if can update
        can_update, error_msg = order.can_update_status(status)
        if not can_update:
            return False, error_msg
        
        # Update status
        success = self.order_repository.update_status(order_id, status.value)
        if success:
            return True, f"Cập nhật trạng thái thành {status.get_display_name()}"
        
        return False, "Đã xảy ra lỗi khi cập nhật"


class CancelOrderUseCase:
    """Use case for cancelling order"""
    
    def __init__(self, order_repository: IOrderRepository, product_repository: IProductRepository):
        self.order_repository = order_repository
        self.product_repository = product_repository
    
    def execute(self, order_id: str, user_id: int) -> tuple[bool, str]:
        """
        Cancel order
        Returns: (success, message)
        """
        # Get order
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return False, "Đơn hàng không tồn tại"
        
        # Check ownership
        if order.user_id != user_id:
            return False, "Bạn không có quyền hủy đơn hàng này"
        
        # Check if can cancel
        if not order.can_cancel():
            return False, "Không thể hủy đơn hàng ở trạng thái hiện tại"
        
        # Update status to cancelled
        success = self.order_repository.update_status(order_id, OrderStatus.CANCELLED.value)
        if success:
            # Restore stock
            for item in order.items:
                product = self.product_repository.get_by_id(item.product_id)
                if product:
                    new_stock = product.stock_quantity + item.quantity
                    self.product_repository.update_stock(item.product_id, new_stock)
            
            return True, "Hủy đơn hàng thành công"
        
        return False, "Đã xảy ra lỗi khi hủy đơn hàng"
