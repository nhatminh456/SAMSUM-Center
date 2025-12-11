from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import MySQL config
from config import MYSQL_CONFIG

# Database helper class
class SamsumDB:
    def __init__(self):
        self.config = MYSQL_CONFIG
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Kết nối MySQL database"""
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)
        except Error as e:
            print(f"Lỗi kết nối MySQL: {e}")
            raise
    
    def close(self):
        """Đóng kết nối"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def get_all_products(self):
        self.connect()
        self.cursor.execute('SELECT * FROM products ORDER BY CAST(id AS UNSIGNED) ASC')
        products = self.cursor.fetchall()
        self.close()
        return products
    
    def get_product_by_id(self, product_id):
        self.connect()
        self.cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
        product = self.cursor.fetchone()
        self.close()
        return product
    
    def get_products_by_category(self, category_id):
        self.connect()
        self.cursor.execute('SELECT * FROM products WHERE categoryID = %s', (category_id,))
        products = self.cursor.fetchall()
        self.close()
        return products
    
    def get_bestseller_products(self):
        self.connect()
        self.cursor.execute('SELECT * FROM products WHERE bestSeller = TRUE')
        products = self.cursor.fetchall()
        self.close()
        return products
    
    def search_products(self, keyword):
        self.connect()
        self.cursor.execute('SELECT * FROM products WHERE tenSP LIKE %s', (f'%{keyword}%',))
        products = self.cursor.fetchall()
        self.close()
        return products
    
    def get_all_categories(self):
        self.connect()
        self.cursor.execute('SELECT * FROM categories')
        categories = self.cursor.fetchall()
        self.close()
        return categories
    
    def check_login(self, email, password):
        self.connect()
        self.cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = self.cursor.fetchone()
        self.close()
        return user
    
    def get_user_by_email(self, email):
        self.connect()
        self.cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = self.cursor.fetchone()
        self.close()
        return user
    
    def register_user(self, user_data):
        self.connect()
        try:
            # Mặc định role là 'user'
            self.cursor.execute('INSERT INTO users (id, email, password, role) VALUES (%s, %s, %s, %s)',
                              (user_data['id'], user_data['email'], user_data['password'], 'user'))
            self.conn.commit()
            self.close()
            return True
        except Error:
            self.close()
            return False
    
    def add_product(self, product_data):
        self.connect()
        self.cursor.execute('''
            INSERT INTO products (id, tenSP, gia, categoryID, image, mota, namSX, thongso, bestSeller)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (product_data['id'], product_data['tenSP'], product_data['gia'], 
              product_data['categoryID'], product_data.get('image'), 
              product_data.get('mota'), product_data.get('namSX'), 
              product_data.get('thongso'), product_data.get('bestSeller', False)))
        self.conn.commit()
        self.close()
        return True
    
    def update_product(self, product_id, product_data):
        self.connect()
        self.cursor.execute('''
            UPDATE products 
            SET tenSP = %s, gia = %s, categoryID = %s, image = %s, mota = %s, namSX = %s, thongso = %s, bestSeller = %s
            WHERE id = %s
        ''', (product_data['tenSP'], product_data['gia'], product_data['categoryID'],
              product_data.get('image'), product_data.get('mota'), 
              product_data.get('namSX'), product_data.get('thongso'),
              product_data.get('bestSeller', False), product_id))
        self.conn.commit()
        self.close()
        return True
    
    def delete_product(self, product_id):
        self.connect()
        self.cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
        self.conn.commit()
        self.close()
        return True
    
    def create_order(self, order_data):
        """Tạo đơn hàng mới"""
        self.connect()
        try:
            # Thêm đơn hàng
            self.cursor.execute('''
                INSERT INTO orders (id, user_id, user_email, total_amount, status, 
                                  shipping_name, shipping_phone, shipping_address, payment_method, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (order_data['id'], order_data['user_id'], order_data['user_email'],
                  order_data['total_amount'], order_data.get('status', 'pending'),
                  order_data.get('shipping_name'), order_data.get('shipping_phone'),
                  order_data.get('shipping_address'), order_data.get('payment_method'),
                  order_data.get('notes')))
            
            # Thêm chi tiết sản phẩm
            for item in order_data['items']:
                self.cursor.execute('''
                    INSERT INTO order_items (order_id, product_id, product_name, product_price, quantity, subtotal)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (order_data['id'], item['product_id'], item['product_name'],
                      item['product_price'], item['quantity'], item['subtotal']))
            
            self.conn.commit()
            self.close()
            return True
        except Error as e:
            print(f"Lỗi tạo đơn hàng: {e}")
            self.close()
            return False
    
    def get_user_orders(self, user_id):
        """Lấy tất cả đơn hàng của user"""
        self.connect()
        self.cursor.execute('''
            SELECT * FROM orders 
            WHERE user_id = %s 
            ORDER BY order_date DESC
        ''', (user_id,))
        orders = self.cursor.fetchall()
        self.close()
        return orders
    
    def get_order_by_id(self, order_id):
        """Lấy thông tin đơn hàng theo ID"""
        self.connect()
        self.cursor.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
        order = self.cursor.fetchone()
        self.close()
        return order
    
    def get_order_items(self, order_id):
        """Lấy chi tiết sản phẩm trong đơn hàng"""
        self.connect()
        self.cursor.execute('SELECT * FROM order_items WHERE order_id = %s', (order_id,))
        items = self.cursor.fetchall()
        self.close()
        return items
    
    def get_all_orders(self):
        """Lấy tất cả đơn hàng (Admin)"""
        self.connect()
        self.cursor.execute('SELECT * FROM orders ORDER BY order_date DESC')
        orders = self.cursor.fetchall()
        self.close()
        return orders
    
    def update_order_status(self, order_id, status):
        """Cập nhật trạng thái đơn hàng"""
        self.connect()
        self.cursor.execute('UPDATE orders SET status = %s WHERE id = %s', (status, order_id))
        self.conn.commit()
        self.close()
        return True

app = Flask(__name__)
app.secret_key = 'samsum-secret-key-2024'

# Initialize database
db = SamsumDB()

#  ADMIN CHECK DECORATOR 

def admin_required(f):
    """Decorator để kiểm tra quyền admin"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập!', 'warning')
            return redirect(url_for('login'))
        
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập trang này!', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

# HOME PAGE

@app.route('/')
def index():
    """Trang chủ - Hiển thị sản phẩm nổi bật"""
    products = db.get_all_products()
    bestsellers = db.get_bestseller_products()
    categories = db.get_all_categories()
    return render_template('index.html', 
                         products=products[:8], 
                         bestsellers=bestsellers,
                         categories=categories)

# PRODUCTS 

@app.route('/products')
def products():
    """Danh sách tất cả sản phẩm"""
    all_products = db.get_all_products()
    categories = db.get_all_categories()
    return render_template('products.html', 
                         products=all_products,
                         categories=categories)

@app.route('/products/category/<int:category_id>')
def products_by_category(category_id):
    """Sản phẩm theo danh mục"""
    category_products = db.get_products_by_category(category_id)
    categories = db.get_all_categories()
    category_name = next((c['tenDM'] for c in categories if c['id'] == category_id), 'Unknown')
    return render_template('products.html', 
                         products=category_products,
                         categories=categories,
                         current_category=category_name)

@app.route('/product/<product_id>')
def product_detail(product_id):
    """Chi tiết sản phẩm"""
    product = db.get_product_by_id(product_id)
    if not product:
        flash('Sản phẩm không tồn tại!', 'danger')
        return redirect(url_for('products'))
    
    # Lấy sản phẩm liên quan (cùng danh mục)
    related = db.get_products_by_category(product['categoryID'])
    related = [p for p in related if p['id'] != product_id][:4]
    
    return render_template('product_detail.html', 
                         product=product,
                         related_products=related)

@app.route('/search')
def search():
    """Tìm kiếm sản phẩm"""
    keyword = request.args.get('q', '')
    if keyword:
        results = db.search_products(keyword)
    else:
        results = []
    
    categories = db.get_all_categories()
    return render_template('products.html', 
                         products=results,
                         categories=categories,
                         search_keyword=keyword)

# AUTHENTICATION 
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Đăng nhập"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = db.check_login(email, password)
        if user:
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_role'] = user.get('role', 'user')  # Lưu role vào session
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email hoặc mật khẩu không đúng!', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Đăng ký tài khoản"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not email or not password:
            flash('Vui lòng điền đầy đủ thông tin!', 'danger')
        elif password != confirm_password:
            flash('Mật khẩu xác nhận không khớp!', 'danger')
        elif len(password) < 3:
            flash('Mật khẩu phải có ít nhất 3 ký tự!', 'danger')
        else:
            # Tạo ID ngẫu nhiên
            import uuid
            user_id = str(uuid.uuid4())[:4]
            
            success = db.register_user({
                'id': user_id,
                'email': email,
                'password': password
            })
            
            if success:
                flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Email đã tồn tại!', 'danger')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Đăng xuất"""
    session.clear()
    flash('Đã đăng xuất!', 'info')
    return redirect(url_for('index'))

#  SHOPPING CART 

@app.route('/cart')
def cart():
    """Xem giỏ hàng"""
    cart_items = session.get('cart', {})
    products_in_cart = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = db.get_product_by_id(product_id)
        if product:
            product['quantity'] = quantity
            product['subtotal'] = product['gia'] * quantity
            products_in_cart.append(product)
            total += product['subtotal']
    
    return render_template('cart.html', 
                         cart_items=products_in_cart,
                         total=total)

@app.route('/cart/add/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Thêm sản phẩm vào giỏ hàng"""
    # Kiểm tra đăng nhập
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng!', 'warning')
        return redirect(url_for('login'))
    
    quantity = int(request.form.get('quantity', 1))
    
    # Kiểm tra sản phẩm có tồn tại không
    product = db.get_product_by_id(product_id)
    if not product:
        flash('Sản phẩm không tồn tại!', 'danger')
        return redirect(url_for('products'))
    
    # Lấy giỏ hàng từ session (hoặc tạo mới)
    cart = session.get('cart', {})
    
    # Thêm hoặc cập nhật số lượng
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    # Lưu lại vào session
    session['cart'] = cart
    session.modified = True
    
    flash(f'Đã thêm {product["tenSP"]} vào giỏ hàng!', 'success')
    return redirect(request.referrer or url_for('products'))

@app.route('/cart/update/<product_id>', methods=['POST'])
def update_cart(product_id):
    """Cập nhật số lượng sản phẩm trong giỏ"""
    quantity = int(request.form.get('quantity', 1))
    
    cart = session.get('cart', {})
    
    if quantity > 0:
        cart[product_id] = quantity
    else:
        # Nếu số lượng = 0, xóa khỏi giỏ
        cart.pop(product_id, None)
    
    session['cart'] = cart
    session.modified = True
    
    flash('Đã cập nhật giỏ hàng!', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/remove/<product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Xóa sản phẩm khỏi giỏ hàng"""
    cart = session.get('cart', {})
    
    if product_id in cart:
        cart.pop(product_id)
        session['cart'] = cart
        session.modified = True
        flash('Đã xóa sản phẩm khỏi giỏ hàng!', 'success')
    
    return redirect(url_for('cart'))

@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    """Xóa toàn bộ giỏ hàng"""
    session.pop('cart', None)
    session.modified = True
    flash('Đã xóa toàn bộ giỏ hàng!', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Thanh toán"""
    cart = session.get('cart', {})
    
    if not cart:
        flash('Giỏ hàng trống!', 'warning')
        return redirect(url_for('products'))
    
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để thanh toán!', 'warning')
        return redirect(url_for('login'))
    
    # Tính tổng tiền
    products_in_cart = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = db.get_product_by_id(product_id)
        if product:
            product['quantity'] = quantity
            product['subtotal'] = product['gia'] * quantity
            products_in_cart.append(product)
            total += product['subtotal']
    
    if request.method == 'POST':
        # Tạo order ID
        import uuid
        from datetime import datetime
        order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:4].upper()}"
        
        # Chuẩn bị dữ liệu đơn hàng
        order_data = {
            'id': order_id,
            'user_id': session['user_id'],
            'user_email': session['user_email'],
            'total_amount': total,
            'status': 'pending',
            'shipping_name': request.form.get('name'),
            'shipping_phone': request.form.get('phone'),
            'shipping_address': request.form.get('address'),
            'payment_method': request.form.get('payment_method', 'COD'),
            'notes': request.form.get('notes'),
            'items': []
        }
        
        # Thêm chi tiết sản phẩm
        for product in products_in_cart:
            order_data['items'].append({
                'product_id': product['id'],
                'product_name': product['tenSP'],
                'product_price': product['gia'],
                'quantity': product['quantity'],
                'subtotal': product['subtotal']
            })
        
        # Lưu đơn hàng vào database
        if db.create_order(order_data):
            session.pop('cart', None)
            session.modified = True
            flash(f'Đặt hàng thành công! Mã đơn hàng: {order_id}', 'success')
            return redirect(url_for('order_history'))
        else:
            flash('Có lỗi xảy ra khi đặt hàng. Vui lòng thử lại!', 'danger')
    
    return render_template('checkout.html', 
                         cart_items=products_in_cart,
                         total=total)

# ORDER HISTORY

@app.route('/orders')
def order_history():
    """Lịch sử đơn hàng của user"""
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để xem lịch sử đơn hàng!', 'warning')
        return redirect(url_for('login'))
    
    orders = db.get_user_orders(session['user_id'])
    return render_template('order_history.html', orders=orders)

@app.route('/order/<order_id>')
def order_detail(order_id):
    """Chi tiết đơn hàng"""
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập!', 'warning')
        return redirect(url_for('login'))
    
    order = db.get_order_by_id(order_id)
    
    if not order:
        flash('Đơn hàng không tồn tại!', 'danger')
        return redirect(url_for('order_history'))
    
    # Kiểm tra quyền xem (user chỉ xem được đơn của mình, admin xem được tất cả)
    if order['user_id'] != session['user_id'] and session.get('user_role') != 'admin':
        flash('Bạn không có quyền xem đơn hàng này!', 'danger')
        return redirect(url_for('order_history'))
    
    items = db.get_order_items(order_id)
    return render_template('order_detail.html', order=order, items=items)

#ADMIN - CRUD OPERATIONS 

@app.route('/admin/products')
@admin_required
def admin_products():
    """Quản lý sản phẩm (Admin)"""
    
    all_products = db.get_all_products()
    categories = db.get_all_categories()
    return render_template('admin_products.html', 
                         products=all_products,
                         categories=categories)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Thêm sản phẩm mới (CREATE)"""
    
    if request.method == 'POST':
        product_data = {
            'id': request.form.get('id'),
            'tenSP': request.form.get('tenSP'),
            'gia': int(request.form.get('gia', 0)),
            'categoryID': int(request.form.get('categoryID', 1)),
            'image': request.form.get('image'),
            'mota': request.form.get('mota'),
            'namSX': int(request.form.get('namSX', 2024)),
            'thongso': request.form.get('thongso'),
            'bestSeller': 'bestSeller' in request.form
        } 
        try:
            db.add_product(product_data)
            flash('Thêm sản phẩm thành công!', 'success')
            return redirect(url_for('admin_products'))
        except Exception as e:
            flash(f'Lỗi: {str(e)}', 'danger')
    
    categories = db.get_all_categories()
    return render_template('admin_add_product.html', categories=categories)

@app.route('/admin/product/edit/<product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    """Sửa sản phẩm (UPDATE)"""
    
    product = db.get_product_by_id(product_id)
    if not product:
        flash('Sản phẩm không tồn tại!', 'danger')
        return redirect(url_for('admin_products'))
    
    if request.method == 'POST':
        product_data = {
            'tenSP': request.form.get('tenSP'),
            'gia': int(request.form.get('gia', 0)),
            'categoryID': int(request.form.get('categoryID', 1)),
            'image': request.form.get('image'),
            'mota': request.form.get('mota'),
            'namSX': int(request.form.get('namSX', 2024)),
            'thongso': request.form.get('thongso'),
            'bestSeller': 'bestSeller' in request.form
        }
        
        try:
            db.update_product(product_id, product_data)
            flash('Cập nhật sản phẩm thành công!', 'success')
            return redirect(url_for('admin_products'))
        except Exception as e:
            flash(f'Lỗi: {str(e)}', 'danger')
    
    categories = db.get_all_categories()
    return render_template('admin_edit_product.html', 
                         product=product,
                         categories=categories)

@app.route('/admin/product/delete/<product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    """Xóa sản phẩm (DELETE)"""
    
    try:
        db.delete_product(product_id)
        flash('Xóa sản phẩm thành công!', 'success')
    except Exception as e:
        flash(f'Lỗi: {str(e)}', 'danger')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    """Quản lý đơn hàng (Admin)"""
    all_orders = db.get_all_orders()
    return render_template('admin_orders.html', orders=all_orders)

@app.route('/admin/order/<order_id>')
@admin_required
def admin_order_detail(order_id):
    """Chi tiết đơn hàng (Admin)"""
    order = db.get_order_by_id(order_id)
    if not order:
        flash('Đơn hàng không tồn tại!', 'danger')
        return redirect(url_for('admin_orders'))
    
    items = db.get_order_items(order_id)
    return render_template('admin_order_detail.html', order=order, items=items)

@app.route('/admin/order/<order_id>/status', methods=['POST'])
@admin_required
def admin_update_order_status(order_id):
    """Cập nhật trạng thái đơn hàng (Admin)"""
    status = request.form.get('status')
    
    if status in ['pending', 'processing', 'shipping', 'delivered', 'cancelled']:
        db.update_order_status(order_id, status)
        flash('Cập nhật trạng thái đơn hàng thành công!', 'success')
    else:
        flash('Trạng thái không hợp lệ!', 'danger')
    
    return redirect(url_for('admin_order_detail', order_id=order_id))

# ERROR HANDLERS 

@app.errorhandler(404)
def page_not_found(e):
    return '<h1>404 - Page Not Found</h1><a href="/">Go Home</a>', 404

@app.errorhandler(500)
def internal_server_error(e):
    return '<h1>500 - Internal Server Error</h1><a href="/">Go Home</a>', 500

# RUN APP 

if __name__ == '__main__':
    print("="*60)
    print("SAMSUM FLASK APP IS RUNNING") 
    print("="*60)
    print("Website: http://localhost:5000")
    print("Admin: http://localhost:5000/admin/products")
    print("="*60)
    app.run(debug=True, port=5000)
