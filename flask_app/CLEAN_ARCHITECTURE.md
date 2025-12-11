"""
Clean Architecture Structure Documentation

📁 Project Structure:
====================

src/
├── domain/                          # Enterprise Business Rules (Innermost Layer)
│   ├── entities/                    # Business objects/models
│   │   ├── user.py                  # User entity with business logic
│   │   ├── product.py               # Product entity with validation
│   │   ├── category.py              # Category entity
│   │   └── order.py                 # Order & OrderItem entities with status management
│   └── repositories/                # Abstract interfaces (Ports)
│       └── interfaces.py            # Repository interfaces (IUserRepository, etc.)
│
├── application/                     # Application Business Rules (Use Cases Layer)
│   └── use_cases/                   # Business logic implementation
│       ├── user_use_cases.py        # Register, Login, Profile operations
│       ├── product_use_cases.py     # CRUD operations for products
│       ├── order_use_cases.py       # Order creation, status management
│       └── category_use_cases.py    # Category operations
│
├── infrastructure/                  # Frameworks & Drivers (Outermost Layer)
│   └── database/                    # Database implementations (Adapters)
│       ├── mysql_user_repository.py
│       ├── mysql_product_repository.py
│       ├── mysql_category_repository.py
│       └── mysql_order_repository.py
│
├── presentation/                    # Interface Adapters
│   └── controllers/                 # Web controllers
│       ├── user_controller.py       # Handle HTTP requests for users
│       ├── product_controller.py    # Handle HTTP requests for products
│       └── order_controller.py      # Handle HTTP requests for orders
│
└── container.py                     # Dependency Injection Container


🏗️ Architecture Layers:
=======================

1. DOMAIN LAYER (Core Business Logic)
   - No dependencies on outer layers
   - Contains entities with business rules
   - Defines repository interfaces (ports)
   - Pure Python, no frameworks

2. APPLICATION LAYER (Use Cases)
   - Depends only on Domain layer
   - Orchestrates business logic
   - Implements use cases/features
   - Framework-agnostic

3. INFRASTRUCTURE LAYER (Technical Details)
   - Implements Domain interfaces
   - Database connections
   - External services
   - Framework-specific code

4. PRESENTATION LAYER (User Interface)
   - Controllers handle HTTP
   - Depends on Application layer
   - Flask routes and views
   - Request/Response handling


🔄 Dependency Flow:
===================

Presentation → Application → Domain ← Infrastructure
                                ↑
                                └─── (implements interfaces)


✅ Benefits:
============

1. ✅ Separation of Concerns
   - Business logic independent from frameworks
   - Each layer has single responsibility

2. ✅ Testability
   - Can test business logic without database
   - Easy to mock dependencies

3. ✅ Maintainability
   - Changes in one layer don't affect others
   - Clear structure, easy to navigate

4. ✅ Flexibility
   - Can swap database (MySQL → PostgreSQL)
   - Can change framework (Flask → FastAPI)
   - Business logic remains unchanged

5. ✅ Scalability
   - Easy to add new features
   - Clear patterns to follow


📋 How to Use:
==============

1. Run the Clean Architecture version:
   ```bash
   python app_clean.py
   ```

2. Compare with original:
   - app.py = Monolithic (all in one file)
   - app_clean.py = Clean Architecture (layered)


🔧 Making Changes:
==================

Add new feature:
1. Create Entity in domain/entities/
2. Add Repository interface in domain/repositories/
3. Implement Use Case in application/use_cases/
4. Implement Repository in infrastructure/database/
5. Create Controller in presentation/controllers/
6. Wire dependencies in container.py
7. Add routes in app_clean.py

Example: Add Review feature
- domain/entities/review.py
- domain/repositories/interfaces.py (add IReviewRepository)
- application/use_cases/review_use_cases.py
- infrastructure/database/mysql_review_repository.py
- presentation/controllers/review_controller.py
- container.py (wire dependencies)
- app_clean.py (add routes)


🎯 Key Concepts:
================

SOLID Principles:
- Single Responsibility: Each class has one job
- Open/Closed: Open for extension, closed for modification
- Liskov Substitution: Can swap implementations
- Interface Segregation: Small, focused interfaces
- Dependency Inversion: Depend on abstractions, not concrete classes

Dependency Injection:
- Dependencies provided from outside
- Managed by DIContainer
- Easy to test and swap

Repository Pattern:
- Abstract data access
- Business logic doesn't know about database
- Can switch databases easily


📚 References:
==============

- Clean Architecture by Robert C. Martin
- Hexagonal Architecture (Ports & Adapters)
- Onion Architecture
- Domain-Driven Design (DDD)
"""
