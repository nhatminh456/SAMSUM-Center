"""User Controller - Handles user-related routes"""
from flask import render_template, request, redirect, url_for, session, flash
from ...application.use_cases import (
    RegisterUserUseCase,
    LoginUserUseCase,
    GetUserProfileUseCase
)
from ...domain.entities import User


class UserController:
    """Controller for user operations"""
    
    def __init__(self, register_use_case: RegisterUserUseCase,
                 login_use_case: LoginUserUseCase,
                 profile_use_case: GetUserProfileUseCase):
        self.register_use_case = register_use_case
        self.login_use_case = login_use_case
        self.profile_use_case = profile_use_case
    
    def show_register_page(self):
        """Show registration page"""
        return render_template('register.html')
    
    def register(self):
        """Handle user registration"""
        if request.method == 'POST':
            user = User(
                username=request.form.get('username', ''),
                email=request.form.get('email', ''),
                password=request.form.get('password', ''),
                full_name=request.form.get('full_name', ''),
                phone=request.form.get('phone', ''),
                address=request.form.get('address', ''),
                role='user'
            )
            
            success, message, user_id = self.register_use_case.execute(user)
            
            if success:
                flash(message, 'success')
                return redirect(url_for('login'))
            else:
                flash(message, 'danger')
                return render_template('register.html')
        
        return self.show_register_page()
    
    def show_login_page(self):
        """Show login page"""
        return render_template('login.html')
    
    def login(self):
        """Handle user login"""
        if request.method == 'POST':
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            
            success, message, user = self.login_use_case.execute(username, password)
            
            if success and user:
                session['user_id'] = user.id
                session['username'] = user.username
                session['user_email'] = user.email
                session['user_role'] = user.role
                flash(message, 'success')
                return redirect(url_for('index'))
            else:
                flash(message, 'danger')
                return render_template('login.html')
        
        return self.show_login_page()
    
    def logout(self):
        """Handle user logout"""
        session.clear()
        flash('Đã đăng xuất thành công', 'success')
        return redirect(url_for('index'))
