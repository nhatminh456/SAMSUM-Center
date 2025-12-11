"""Dependency Injection Container"""
from config import MYSQL_CONFIG
from .infrastructure.database import (
    MySQLUserRepository,
    MySQLProductRepository,
    MySQLCategoryRepository,
    MySQLOrderRepository
)
from .application.use_cases import (
    # User
    RegisterUserUseCase,
    LoginUserUseCase,
    GetUserProfileUseCase,
    UpdateUserProfileUseCase,
    # Product
    GetAllProductsUseCase,
    GetProductByIdUseCase,
    GetProductsByCategoryUseCase,
    SearchProductsUseCase,
    CreateProductUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase,
    # Order
    CreateOrderUseCase,
    GetUserOrdersUseCase,
    GetOrderByIdUseCase,
    GetAllOrdersUseCase,
    UpdateOrderStatusUseCase,
    CancelOrderUseCase,
    # Category
    GetAllCategoriesUseCase,
    GetCategoryByIdUseCase
)
from .presentation.controllers import (
    UserController,
    ProductController,
    OrderController
)


class DIContainer:
    """Dependency Injection Container for managing dependencies"""
    
    def __init__(self, db_config: dict):
        self.db_config = db_config
        
        # Repositories (Infrastructure Layer)
        self.user_repository = MySQLUserRepository(db_config)
        self.product_repository = MySQLProductRepository(db_config)
        self.category_repository = MySQLCategoryRepository(db_config)
        self.order_repository = MySQLOrderRepository(db_config)
        
        # Use Cases (Application Layer)
        self._init_user_use_cases()
        self._init_product_use_cases()
        self._init_order_use_cases()
        self._init_category_use_cases()
        
        # Controllers (Presentation Layer)
        self._init_controllers()
    
    def _init_user_use_cases(self):
        """Initialize user use cases"""
        self.register_user_use_case = RegisterUserUseCase(self.user_repository)
        self.login_user_use_case = LoginUserUseCase(self.user_repository)
        self.get_user_profile_use_case = GetUserProfileUseCase(self.user_repository)
        self.update_user_profile_use_case = UpdateUserProfileUseCase(self.user_repository)
    
    def _init_product_use_cases(self):
        """Initialize product use cases"""
        self.get_all_products_use_case = GetAllProductsUseCase(self.product_repository)
        self.get_product_by_id_use_case = GetProductByIdUseCase(self.product_repository)
        self.get_products_by_category_use_case = GetProductsByCategoryUseCase(self.product_repository)
        self.search_products_use_case = SearchProductsUseCase(self.product_repository)
        self.create_product_use_case = CreateProductUseCase(self.product_repository)
        self.update_product_use_case = UpdateProductUseCase(self.product_repository)
        self.delete_product_use_case = DeleteProductUseCase(self.product_repository)
    
    def _init_order_use_cases(self):
        """Initialize order use cases"""
        self.create_order_use_case = CreateOrderUseCase(
            self.order_repository, 
            self.product_repository
        )
        self.get_user_orders_use_case = GetUserOrdersUseCase(self.order_repository)
        self.get_order_by_id_use_case = GetOrderByIdUseCase(self.order_repository)
        self.get_all_orders_use_case = GetAllOrdersUseCase(self.order_repository)
        self.update_order_status_use_case = UpdateOrderStatusUseCase(self.order_repository)
        self.cancel_order_use_case = CancelOrderUseCase(
            self.order_repository,
            self.product_repository
        )
    
    def _init_category_use_cases(self):
        """Initialize category use cases"""
        self.get_all_categories_use_case = GetAllCategoriesUseCase(self.category_repository)
        self.get_category_by_id_use_case = GetCategoryByIdUseCase(self.category_repository)
    
    def _init_controllers(self):
        """Initialize controllers"""
        self.user_controller = UserController(
            self.register_user_use_case,
            self.login_user_use_case,
            self.get_user_profile_use_case
        )
        
        self.product_controller = ProductController(
            self.get_all_products_use_case,
            self.get_product_by_id_use_case,
            self.get_products_by_category_use_case,
            self.search_products_use_case,
            self.create_product_use_case,
            self.update_product_use_case,
            self.delete_product_use_case
        )
        
        self.order_controller = OrderController(
            self.create_order_use_case,
            self.get_user_orders_use_case,
            self.get_order_by_id_use_case,
            self.get_all_orders_use_case,
            self.update_order_status_use_case
        )


# Global container instance
container = DIContainer(MYSQL_CONFIG)
