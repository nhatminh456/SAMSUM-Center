"""
SAMSUM Center - Samsung E-commerce Application
Clean Architecture Implementation
"""
from flask import Flask, render_template, request, session
from config import SECRET_KEY
from src.container import container

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY

# Get controllers from DI container
user_controller = container.user_controller
product_controller = container.product_controller
order_controller = container.order_controller

# Get use cases for home page
get_all_products = container.get_all_products_use_case
get_all_categories = container.get_all_categories_use_case


# ============================================
# HOME & PUBLIC ROUTES
# ============================================

@app.route('/')
def index():
    """Home page with featured products"""
    products = get_all_products.execute()
    categories = get_all_categories.execute()
    return render_template('index.html', products=products[:6], categories=categories)


# ============================================
# USER ROUTES
# ============================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    return user_controller.register()


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    return user_controller.login()


@app.route('/logout')
def logout():
    """User logout"""
    return user_controller.logout()


# ============================================
# PRODUCT ROUTES
# ============================================

@app.route('/products')
def products():
    """List all products"""
    return product_controller.list_products()


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    return product_controller.show_product_detail(product_id)


@app.route('/products/category/<int:category_id>')
def products_by_category(category_id):
    """Products by category"""
    return product_controller.products_by_category(category_id)


@app.route('/products/search')
def search_products():
    """Search products"""
    return product_controller.search_products()


# ============================================
# CART & ORDER ROUTES
# ============================================

@app.route('/cart')
def cart():
    """Shopping cart"""
    return order_controller.show_cart()


@app.route('/cart/add/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    """Add product to cart"""
    return order_controller.add_to_cart(product_id)


@app.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    """Update cart quantity"""
    return order_controller.update_cart(product_id)


@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Remove product from cart"""
    return order_controller.remove_from_cart(product_id)


@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    """Clear cart"""
    return order_controller.clear_cart()


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout page"""
    if request.method == 'POST':
        return order_controller.checkout()
    return order_controller.show_checkout()


@app.route('/orders')
def orders():
    """User order history"""
    return order_controller.user_orders()


@app.route('/order/<order_id>')
def order_detail(order_id):
    """Order detail"""
    return order_controller.order_detail(order_id)


# ============================================
# ADMIN ROUTES - PRODUCTS
# ============================================

@app.route('/admin/products')
def admin_products():
    """Admin: List products"""
    return product_controller.admin_list_products()


@app.route('/admin/product/add', methods=['GET', 'POST'])
def admin_add_product():
    """Admin: Add product"""
    return product_controller.admin_add_product()


@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    """Admin: Edit product"""
    return product_controller.admin_edit_product(product_id)


@app.route('/admin/product/delete/<int:product_id>')
def admin_delete_product(product_id):
    """Admin: Delete product"""
    return product_controller.admin_delete_product(product_id)


# ============================================
# ADMIN ROUTES - ORDERS
# ============================================

@app.route('/admin/orders')
def admin_orders():
    """Admin: List all orders"""
    return order_controller.admin_orders()


@app.route('/admin/order/<order_id>')
def admin_order_detail(order_id):
    """Admin: Order detail"""
    return order_controller.admin_order_detail(order_id)


@app.route('/admin/order/<order_id>/status', methods=['POST'])
def admin_update_order_status(order_id):
    """Admin: Update order status"""
    return order_controller.admin_update_order_status(order_id)


# ============================================
# TEMPLATE CONTEXT
# ============================================

@app.context_processor
def inject_categories():
    """Inject categories into all templates"""
    categories = get_all_categories.execute()
    return dict(categories=categories)




@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html'), 500


# ============================================
# RUN APPLICATION
# ============================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
