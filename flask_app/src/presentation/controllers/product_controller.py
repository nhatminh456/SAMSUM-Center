"""Product Controller - Handles product-related routes"""
import os
import uuid
from urllib.parse import urlparse, parse_qs, unquote
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from ...application.use_cases import (
    GetAllProductsUseCase,
    GetProductByIdUseCase,
    GetProductsByCategoryUseCase,
    SearchProductsUseCase,
    CreateProductUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase
)
from ...domain.entities import Product


class ProductController:
    """Controller for product operations"""

    _ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    
    def __init__(self, get_all_use_case: GetAllProductsUseCase,
                 get_by_id_use_case: GetProductByIdUseCase,
                 get_by_category_use_case: GetProductsByCategoryUseCase,
                 search_use_case: SearchProductsUseCase,
                 create_use_case: CreateProductUseCase,
                 update_use_case: UpdateProductUseCase,
                 delete_use_case: DeleteProductUseCase,
                 get_all_categories_use_case):
        self.get_all_use_case = get_all_use_case
        self.get_by_id_use_case = get_by_id_use_case
        self.get_by_category_use_case = get_by_category_use_case
        self.search_use_case = search_use_case
        self.create_use_case = create_use_case
        self.update_use_case = update_use_case
        self.delete_use_case = delete_use_case
        self.get_all_categories_use_case = get_all_categories_use_case

    def _save_uploaded_image(self, image_file):
        """Save uploaded image to static/images and return stored filename"""
        if not image_file or not image_file.filename:
            return None

        original_name = secure_filename(image_file.filename)
        if not original_name:
            raise ValueError('Tên file ảnh không hợp lệ')

        _, ext = os.path.splitext(original_name)
        ext = ext.lower()
        if ext not in self._ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError('Chỉ hỗ trợ ảnh: .jpg, .jpeg, .png, .gif, .webp, .bmp')

        stored_name = f"{uuid.uuid4().hex}{ext}"
        upload_dir = os.path.join('static', 'images')
        os.makedirs(upload_dir, exist_ok=True)
        image_file.save(os.path.join(upload_dir, stored_name))
        return stored_name

    def _normalize_image_url(self, image_url: str) -> str:
        """Normalize URL input; convert Google imgres URL to direct image URL when possible."""
        image_text = (image_url or '').strip()
        if not image_text:
            return ''

        lower = image_text.lower()
        if 'google.com/imgres' in lower and 'imgurl=' in lower:
            try:
                parsed = urlparse(image_text)
                params = parse_qs(parsed.query)
                direct = params.get('imgurl', [''])[0]
                direct = unquote(direct).strip()
                if direct:
                    return direct
            except Exception:
                return image_text

        return image_text
    
    def list_products(self):
        """Show all products"""
        products = self.get_all_use_case.execute()
        return render_template('products.html', products=products)
    
    def show_product_detail(self, product_id):
        """Show product detail"""
        product = self.get_by_id_use_case.execute(product_id)
        if not product:
            flash('Sản phẩm không tồn tại', 'danger')
            return redirect(url_for('products'))
        
        return render_template('product_detail.html', product=product)
    
    def products_by_category(self, category_id):
        """Show products by category"""
        products = self.get_by_category_use_case.execute(category_id)
        return render_template('products.html', products=products, category_id=category_id)
    
    def search_products(self):
        """Search products"""
        keyword = request.args.get('q', '')
        products = self.search_use_case.execute(keyword)
        return render_template('products.html', products=products, keyword=keyword)
    
    # Admin operations
    def admin_list_products(self):
        """Admin: List all products"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        products = self.get_all_use_case.execute()
        return render_template('admin_products.html', products=products)
    
    def admin_show_add_product(self):
        """Admin: Show add product form"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        categories = self.get_all_categories_use_case.execute()
        return render_template('admin_add_product.html', categories=categories)
    
    def admin_add_product(self):
        """Admin: Add new product"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            try:
                price_val = float(request.form.get('price', 0) or 0)
                cat_val = int(request.form.get('category_id', 0) or 0)
                stock_val = int(request.form.get('stock_quantity', 0) or 0)
            except (ValueError, TypeError):
                flash('Dữ liệu không hợp lệ (giá, danh mục hoặc số lượng)', 'danger')
                categories = self.get_all_categories_use_case.execute()
                return render_template('admin_add_product.html', categories=categories)

            image_url = self._normalize_image_url(request.form.get('image_url', ''))
            try:
                uploaded_file_name = self._save_uploaded_image(request.files.get('image_file'))
                if uploaded_file_name:
                    image_url = uploaded_file_name
            except ValueError as e:
                flash(str(e), 'danger')
                categories = self.get_all_categories_use_case.execute()
                return render_template('admin_add_product.html', categories=categories)

            product = Product(
                name=request.form.get('name', ''),
                description=request.form.get('description', ''),
                price=price_val,
                category_id=cat_val,
                image_url=image_url,
                stock_quantity=stock_val
            )
            
            success, message, product_id = self.create_use_case.execute(product)
            
            if success:
                flash(message, 'success')
                return redirect(url_for('admin_products'))
            else:
                flash(message, 'danger')
        
        categories = self.get_all_categories_use_case.execute()
        return render_template('admin_add_product.html', categories=categories)
    
    def admin_show_edit_product(self, product_id):
        """Admin: Show edit product form"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        product = self.get_by_id_use_case.execute(product_id)
        if not product:
            flash('Sản phẩm không tồn tại', 'danger')
            return redirect(url_for('admin_products'))
        
        categories = self.get_all_categories_use_case.execute()
        return render_template('admin_edit_product.html', product=product, categories=categories)
    
    def admin_edit_product(self, product_id):
        """Admin: Edit product"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        product = self.get_by_id_use_case.execute(product_id)
        if not product:
            flash('Sản phẩm không tồn tại', 'danger')
            return redirect(url_for('admin_products'))
        
        if request.method == 'POST':
            try:
                price_val = float(request.form.get('price', 0) or 0)
                cat_val = int(request.form.get('category_id', 0) or 0)
                stock_val = int(request.form.get('stock_quantity', 0) or 0)
            except (ValueError, TypeError):
                flash('Dữ liệu không hợp lệ (giá, danh mục hoặc số lượng)', 'danger')
                return self.admin_show_edit_product(product_id)

            image_url = self._normalize_image_url(request.form.get('image_url', ''))
            try:
                uploaded_file_name = self._save_uploaded_image(request.files.get('image_file'))
                if uploaded_file_name:
                    image_url = uploaded_file_name
            except ValueError as e:
                flash(str(e), 'danger')
                return self.admin_show_edit_product(product_id)

            product = Product(
                id=product_id,
                name=request.form.get('name', ''),
                description=request.form.get('description', ''),
                price=price_val,
                category_id=cat_val,
                image_url=image_url,
                stock_quantity=stock_val
            )
            
            success, message = self.update_use_case.execute(product)
            
            if success:
                flash(message, 'success')
                return redirect(url_for('admin_products'))
            else:
                flash(message, 'danger')
        
        return self.admin_show_edit_product(product_id)
    
    def admin_delete_product(self, product_id):
        """Admin: Delete product"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        success, message = self.delete_use_case.execute(product_id)
        flash(message, 'success' if success else 'danger')
        return redirect(url_for('admin_products'))
