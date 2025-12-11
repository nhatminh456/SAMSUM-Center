"""Product Entity - Domain Model"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    """Product domain entity representing a Samsung product"""
    
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    price: float = 0.0
    category_id: int = 0
    category_name: Optional[str] = None
    image_url: str = ""
    stock_quantity: int = 0
    bestSeller: int = 0
    created_at: Optional[datetime] = None
    
    def is_available(self) -> bool:
        """Check if product is available for purchase"""
        return self.stock_quantity > 0
    
    def can_purchase(self, quantity: int) -> tuple[bool, str]:
        """Check if can purchase given quantity"""
        if quantity <= 0:
            return False, "Số lượng phải lớn hơn 0"
        
        if not self.is_available():
            return False, "Sản phẩm đã hết hàng"
        
        if quantity > self.stock_quantity:
            return False, f"Chỉ còn {self.stock_quantity} sản phẩm"
        
        return True, ""
    
    def formatted_price(self) -> str:
        """Get formatted price in VND"""
        return f"{int(self.price):,}₫"
    
    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category_id': self.category_id,
            'category_name': self.category_name,
            'image_url': self.image_url,
            'stock_quantity': self.stock_quantity,
            'created_at': self.created_at
        }
