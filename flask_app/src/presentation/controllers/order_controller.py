"""Order Controller - Handles order-related routes"""
from flask import render_template, request, redirect, url_for, session, flash
from ...application.use_cases import (
    CreateOrderUseCase,
    GetUserOrdersUseCase,
    GetOrderByIdUseCase,
    GetAllOrdersUseCase,
    UpdateOrderStatusUseCase
)
from ...domain.entities import Order, OrderItem, OrderStatus


class OrderController:
    """Controller for order operations"""
    
    def __init__(self, create_use_case: CreateOrderUseCase,
                 get_user_orders_use_case: GetUserOrdersUseCase,
                 get_by_id_use_case: GetOrderByIdUseCase,
                 get_all_use_case: GetAllOrdersUseCase,
                 update_status_use_case: UpdateOrderStatusUseCase):
        self.create_use_case = create_use_case
        self.get_user_orders_use_case = get_user_orders_use_case
        self.get_by_id_use_case = get_by_id_use_case
        self.get_all_use_case = get_all_use_case
        self.update_status_use_case = update_status_use_case
    
    def _get_cart_with_details(self):
        """Get cart with product details"""
        from ...application.use_cases import GetProductByIdUseCase
        from src.container import container
        
        cart = session.get('cart', {})
        cart_items = []
        total = 0
        
        for product_id, item in cart.items():
            product = container.get_product_by_id_use_case.execute(int(product_id))
            if product:
                cart_item = {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url,
                    'quantity': item['quantity'],
                    'subtotal': product.price * item['quantity']
                }
                cart_items.append(cart_item)
                total += cart_item['subtotal']
        
        return cart_items, total
    
    def show_cart(self):
        """Show shopping cart"""
        cart_items, total = self._get_cart_with_details()
        return render_template('cart.html', cart=cart_items, total=total)
    
    def add_to_cart(self, product_id):
        """Add product to cart"""
        from src.container import container
        
        # Get product details
        product = container.get_product_by_id_use_case.execute(product_id)
        if not product:
            flash('Sản phẩm không tồn tại', 'danger')
            return redirect(url_for('products'))
        
        cart = session.get('cart', {})
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            cart[product_id_str]['quantity'] += 1
        else:
            cart[product_id_str] = {'quantity': 1}
        
        session['cart'] = cart
        flash(f'Đã thêm {product.name} vào giỏ hàng', 'success')
        return redirect(request.referrer or url_for('products'))
    
    def update_cart(self, product_id):
        """Update cart quantity"""
        if request.method == 'POST':
            quantity = int(request.form.get('quantity', 1))
            cart = session.get('cart', {})
            product_id_str = str(product_id)
            
            if product_id_str in cart:
                if quantity > 0:
                    cart[product_id_str]['quantity'] = quantity
                    flash('Đã cập nhật giỏ hàng', 'success')
                else:
                    del cart[product_id_str]
                    flash('Đã xóa sản phẩm khỏi giỏ hàng', 'success')
                
                session['cart'] = cart
        
        return redirect(url_for('cart'))
    
    def remove_from_cart(self, product_id):
        """Remove product from cart"""
        cart = session.get('cart', {})
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            del cart[product_id_str]
            session['cart'] = cart
            flash('Đã xóa sản phẩm khỏi giỏ hàng', 'success')
        
        return redirect(url_for('cart'))
    
    def clear_cart(self):
        """Clear all cart"""
        session['cart'] = {}
        flash('Đã xóa tất cả sản phẩm trong giỏ hàng', 'success')
        return redirect(url_for('cart'))
    
    def show_checkout(self):
        """Show checkout page"""
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để thanh toán', 'warning')
            return redirect(url_for('login'))
        
        cart = session.get('cart', {})
        if not cart:
            flash('Giỏ hàng trống', 'warning')
            return redirect(url_for('products'))
        
        cart_items, total = self._get_cart_with_details()
        return render_template('checkout.html', cart=cart_items, total=total)
    
    def checkout(self):
        """Process checkout"""
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để thanh toán', 'warning')
            return redirect(url_for('login'))
        
        cart = session.get('cart', {})
        if not cart:
            flash('Giỏ hàng trống', 'warning')
            return redirect(url_for('products'))
        
        if request.method == 'POST':
            # Create order entity
            order = Order(
                user_id=session['user_id'],
                customer_name=request.form.get('customer_name', ''),
                customer_phone=request.form.get('customer_phone', ''),
                customer_address=request.form.get('customer_address', ''),
                payment_method=request.form.get('payment_method', 'cod')
            )
            
            # Get cart with details
            cart_items, _ = self._get_cart_with_details()
            
            # Add items from cart
            for item in cart_items:
                order_item = OrderItem(
                    product_id=item['id'],
                    product_name=item['name'],
                    product_price=item['price'],
                    quantity=item['quantity']
                )
                order_item.calculate_subtotal()
                order.add_item(order_item)
            
            # Execute use case
            success, message, order_id = self.create_use_case.execute(order)
            
            if success:
                session['cart'] = {}
                flash(message, 'success')
                return redirect(url_for('order_detail', order_id=order_id))
            else:
                flash(message, 'danger')
        
        return self.show_checkout()
    
    def user_orders(self):
        """Show user's orders"""
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập', 'warning')
            return redirect(url_for('login'))
        
        orders = self.get_user_orders_use_case.execute(session['user_id'])
        return render_template('order_history.html', orders=orders)
    
    def order_detail(self, order_id):
        """Show order detail"""
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập', 'warning')
            return redirect(url_for('login'))
        
        order = self.get_by_id_use_case.execute(order_id)
        if not order:
            flash('Đơn hàng không tồn tại', 'danger')
            return redirect(url_for('orders'))
        
        if order.user_id != session['user_id'] and session.get('user_role') != 'admin':
            flash('Bạn không có quyền xem đơn hàng này', 'danger')
            return redirect(url_for('orders'))
        
        return render_template('order_detail.html', order=order)
    
    # Admin operations
    def admin_orders(self):
        """Admin: List all orders"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        orders = self.get_all_use_case.execute()
        return render_template('admin_orders.html', orders=orders)
    
    def admin_order_detail(self, order_id):
        """Admin: Show order detail"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        order = self.get_by_id_use_case.execute(order_id)
        if not order:
            flash('Đơn hàng không tồn tại', 'danger')
            return redirect(url_for('admin_orders'))
        
        return render_template('admin_order_detail.html', order=order)
    
    def admin_update_order_status(self, order_id):
        """Admin: Update order status"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            new_status = request.form.get('status', '')
            success, message = self.update_status_use_case.execute(order_id, new_status)
            flash(message, 'success' if success else 'danger')
        
        return redirect(url_for('admin_order_detail', order_id=order_id))
