"""Repository Interfaces - Port definitions for data access"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities import User, Product, Category, Order, OrderItem


class IUserRepository(ABC):
    """Interface for User data access"""
    
    @abstractmethod
    def create(self, user: User) -> Optional[int]:
        """Create new user"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    def update(self, user: User) -> bool:
        """Update user"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete user"""
        pass


class IProductRepository(ABC):
    """Interface for Product data access"""
    
    @abstractmethod
    def create(self, product: Product) -> Optional[int]:
        """Create new product"""
        pass
    
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Product]:
        """Get all products"""
        pass
    
    @abstractmethod
    def get_by_category(self, category_id: int) -> List[Product]:
        """Get products by category"""
        pass
    
    @abstractmethod
    def search(self, keyword: str) -> List[Product]:
        """Search products by keyword"""
        pass
    
    @abstractmethod
    def update(self, product: Product) -> bool:
        """Update product"""
        pass
    
    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Delete product"""
        pass
    
    @abstractmethod
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Update product stock quantity"""
        pass


class ICategoryRepository(ABC):
    """Interface for Category data access"""
    
    @abstractmethod
    def create(self, category: Category) -> Optional[int]:
        """Create new category"""
        pass
    
    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Category]:
        """Get all categories"""
        pass
    
    @abstractmethod
    def update(self, category: Category) -> bool:
        """Update category"""
        pass
    
    @abstractmethod
    def delete(self, category_id: int) -> bool:
        """Delete category"""
        pass


class IOrderRepository(ABC):
    """Interface for Order data access"""
    
    @abstractmethod
    def create(self, order: Order) -> Optional[str]:
        """Create new order with items"""
        pass
    
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by ID with items"""
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Order]:
        """Get all orders by user"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Order]:
        """Get all orders"""
        pass
    
    @abstractmethod
    def update_status(self, order_id: str, status: str) -> bool:
        """Update order status"""
        pass
