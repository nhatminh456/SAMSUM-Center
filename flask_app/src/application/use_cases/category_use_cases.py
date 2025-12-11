"""Category Use Cases - Application Business Logic"""
from typing import List, Optional
from ...domain.entities import Category
from ...domain.repositories import ICategoryRepository


class GetAllCategoriesUseCase:
    """Use case for getting all categories"""
    
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository
    
    def execute(self) -> List[Category]:
        """Get all categories"""
        return self.category_repository.get_all()


class GetCategoryByIdUseCase:
    """Use case for getting category by ID"""
    
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository
    
    def execute(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        return self.category_repository.get_by_id(category_id)
