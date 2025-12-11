"""Category Entity - Domain Model"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    """Category domain entity for product classification"""
    
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    
    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
