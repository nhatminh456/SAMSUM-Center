"""Product Use Cases - Application Business Logic"""
from typing import List, Optional
from ...domain.entities import Product
from ...domain.repositories import IProductRepository


class GetAllProductsUseCase:
    """Use case for getting all products"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    def execute(self) -> List[Product]:
        """Get all products"""
        return self.product_repository.get_all()


class GetProductByIdUseCase:
    """Use case for getting product by ID"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    def execute(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.product_repository.get_by_id(product_id)


class GetProductsByCategoryUseCase:
    """Use case for getting products by category"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    def execute(self, category_id: int) -> List[Product]:
        """Get products by category"""
        return self.product_repository.get_by_category(category_id)


class SearchProductsUseCase:
    """Use case for searching products"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    def execute(self, keyword: str) -> List[Product]:
        """Search products by keyword"""
        if not keyword or len(keyword) < 2:
            return []
        return self.product_repository.search(keyword)


class CreateProductUseCase:
    """Use case for creating product (admin)"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    def execute(self, product: Product) -> tuple[bool, str, Optional[int]]:
        """
        Create new product
        Returns: (success, message, product_id)
        """
        # Validate product data
        if not product.name:
            return False, "Tên sản phẩm không được để trống", None
        
        if product.price <= 0:
            return False, "Giá sản phẩm phải lớn hơn 0", None
        
        if product.stock_quantity < 0:
            return False, "Số lượng không được âm", None
        
        # Create product
        product_id = self.product_repository.create(product)
        if product_id:
            return True, "Tạo sản phẩm thành công", product_id
        
        return False, "Đã xảy ra lỗi khi tạo sản phẩm", None


class UpdateProductUseCase:
    """Use case for updating product (admin)"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    def execute(self, product: Product) -> tuple[bool, str]:
        """
        Update product
        Returns: (success, message)
        """
        if not product.id:
            return False, "Product ID không hợp lệ"
        
        # Validate product data
        if not product.name:
            return False, "Tên sản phẩm không được để trống"
        
        if product.price <= 0:
            return False, "Giá sản phẩm phải lớn hơn 0"
        
        success = self.product_repository.update(product)
        if success:
            return True, "Cập nhật sản phẩm thành công"
        
        return False, "Đã xảy ra lỗi khi cập nhật"


class DeleteProductUseCase:
    """Use case for deleting product (admin)"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    def execute(self, product_id: int) -> tuple[bool, str]:
        """
        Delete product
        Returns: (success, message)
        """
        success = self.product_repository.delete(product_id)
        if success:
            return True, "Xóa sản phẩm thành công"
        
        return False, "Đã xảy ra lỗi khi xóa"
