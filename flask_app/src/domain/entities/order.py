"""Order Entities - Domain Models"""
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    """Order status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPING = "shipping"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
    @classmethod
    def from_string(cls, status: str) -> 'OrderStatus':
        """Create OrderStatus from string"""
        try:
            return cls(status.lower())
        except ValueError:
            return cls.PENDING
    
    def get_badge_class(self) -> str:
        """Get Bootstrap badge class for status"""
        badge_map = {
            self.PENDING: "warning",
            self.PROCESSING: "info",
            self.SHIPPING: "primary",
            self.DELIVERED: "success",
            self.CANCELLED: "danger"
        }
        return badge_map.get(self, "secondary")
    
    def get_display_name(self) -> str:
        """Get Vietnamese display name"""
        name_map = {
            self.PENDING: "Chờ xử lý",
            self.PROCESSING: "Đang xử lý",
            self.SHIPPING: "Đang giao",
            self.DELIVERED: "Đã giao",
            self.CANCELLED: "Đã hủy"
        }
        return name_map.get(self, "Không xác định")


@dataclass
class OrderItem:
    """Order item domain entity"""
    
    id: Optional[int] = None
    order_id: Optional[str] = None
    product_id: int = 0
    product_name: str = ""
    product_price: float = 0.0
    quantity: int = 1
    subtotal: float = 0.0
    
    def calculate_subtotal(self) -> float:
        """Calculate subtotal for this item"""
        self.subtotal = self.product_price * self.quantity
        return self.subtotal
    
    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_price': self.product_price,
            'quantity': self.quantity,
            'subtotal': self.subtotal
        }


@dataclass
class Order:
    """Order domain entity"""
    
    id: Optional[str] = None
    user_id: int = 0
    customer_name: str = ""
    customer_phone: str = ""
    customer_address: str = ""
    payment_method: str = "cod"
    total_amount: float = 0.0
    status: OrderStatus = OrderStatus.PENDING
    created_at: Optional[datetime] = None
    items: List[OrderItem] = field(default_factory=list)
    
    def add_item(self, item: OrderItem) -> None:
        """Add item to order"""
        item.order_id = self.id
        self.items.append(item)
    
    def calculate_total(self) -> float:
        """Calculate total amount from items"""
        self.total_amount = sum(item.calculate_subtotal() for item in self.items)
        return self.total_amount
    
    def is_valid(self) -> tuple[bool, str]:
        """Validate order data"""
        if not self.customer_name:
            return False, "Tên khách hàng không được để trống"
        
        if not self.customer_phone:
            return False, "Số điện thoại không được để trống"
        
        if not self.customer_address:
            return False, "Địa chỉ không được để trống"
        
        if not self.items:
            return False, "Đơn hàng phải có ít nhất 1 sản phẩm"
        
        if self.total_amount <= 0:
            return False, "Tổng tiền phải lớn hơn 0"
        
        return True, ""
    
    def can_cancel(self) -> bool:
        """Check if order can be cancelled"""
        return self.status in [OrderStatus.PENDING, OrderStatus.PROCESSING]
    
    def can_update_status(self, new_status: OrderStatus) -> tuple[bool, str]:
        """Check if can update to new status"""
        if self.status == OrderStatus.CANCELLED:
            return False, "Không thể cập nhật đơn hàng đã hủy"
        
        if self.status == OrderStatus.DELIVERED:
            return False, "Không thể cập nhật đơn hàng đã giao"
        
        return True, ""
    
    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_address': self.customer_address,
            'payment_method': self.payment_method,
            'total_amount': self.total_amount,
            'status': self.status.value,
            'created_at': self.created_at,
            'items': [item.to_dict() for item in self.items]
        }
