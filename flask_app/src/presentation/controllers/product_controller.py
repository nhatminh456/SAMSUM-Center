"""Product Controller - Handles product-related routes"""
from flask import render_template, request, redirect, url_for, session, flash
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
    
    def __init__(self, get_all_use_case: GetAllProductsUseCase,
                 get_by_id_use_case: GetProductByIdUseCase,
                 get_by_category_use_case: GetProductsByCategoryUseCase,
                 search_use_case: SearchProductsUseCase,
                 create_use_case: CreateProductUseCase,
                 update_use_case: UpdateProductUseCase,
                 delete_use_case: DeleteProductUseCase):
        self.get_all_use_case = get_all_use_case
        self.get_by_id_use_case = get_by_id_use_case
        self.get_by_category_use_case = get_by_category_use_case
        self.search_use_case = search_use_case
        self.create_use_case = create_use_case
        self.update_use_case = update_use_case
        self.delete_use_case = delete_use_case
    
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
        
        return render_template('admin_add_product.html')
    
    def admin_add_product(self):
        """Admin: Add new product"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            product = Product(
                name=request.form.get('name', ''),
                description=request.form.get('description', ''),
                price=float(request.form.get('price', 0)),
                category_id=int(request.form.get('category_id', 0)),
                image_url=request.form.get('image_url', ''),
                stock_quantity=int(request.form.get('stock_quantity', 0))
            )
            
            success, message, product_id = self.create_use_case.execute(product)
            
            if success:
                flash(message, 'success')
                return redirect(url_for('admin_products'))
            else:
                flash(message, 'danger')
        
        return render_template('admin_add_product.html')
    
    def admin_show_edit_product(self, product_id):
        """Admin: Show edit product form"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        product = self.get_by_id_use_case.execute(product_id)
        if not product:
            flash('Sản phẩm không tồn tại', 'danger')
            return redirect(url_for('admin_products'))
        
        return render_template('admin_edit_product.html', product=product)
    
    def admin_edit_product(self, product_id):
        """Admin: Edit product"""
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập', 'danger')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            product = Product(
                id=product_id,
                name=request.form.get('name', ''),
                description=request.form.get('description', ''),
                price=float(request.form.get('price', 0)),
                category_id=int(request.form.get('category_id', 0)),
                image_url=request.form.get('image_url', ''),
                stock_quantity=int(request.form.get('stock_quantity', 0))
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
