// ===== MODERN SAMSUM CENTER - ENHANCED INTERACTIONS =====

// Page load animation
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// Auto-hide flash messages with fade effect
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert, index) => {
        // Stagger animation
        alert.style.animationDelay = `${index * 0.1}s`;
        
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 300);
        }, 5000);
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.15)';
        navbar.style.padding = '0.5rem 0';
    } else {
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
        navbar.style.padding = '1rem 0';
    }
    
    lastScroll = currentScroll;
});

// Product card hover effect with tilt
document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('mousemove', function(e) {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px) scale(1.02)`;
    });
    
    card.addEventListener('mouseleave', function() {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0) scale(1)';
    });
});

// Smooth add to cart animation
function showCartNotification(productName) {
    const notification = document.createElement('div');
    notification.className = 'cart-notification';
    notification.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>Đã thêm "${productName}" vào giỏ hàng!</span>
    `;
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 50px;
        box-shadow: 0 8px 32px rgba(40, 167, 69, 0.4);
        z-index: 9999;
        animation: slideInRight 0.5s ease;
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 600;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.5s ease';
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

// Cart badge pulse animation
const cartBadge = document.querySelector('.position-relative .badge');
if (cartBadge) {
    setInterval(() => {
        cartBadge.style.animation = 'none';
        setTimeout(() => {
            cartBadge.style.animation = 'pulse 2s infinite';
        }, 10);
    }, 5000);
}

// Format price input with thousands separator
function formatPrice(input) {
    let value = input.value.replace(/\D/g, '');
    if (value) {
        value = parseInt(value).toLocaleString('vi-VN');
    }
    input.value = value;
}

// Enhanced delete confirmation
function confirmDelete(productName) {
    return confirm(`⚠️ Xác nhận xóa\n\nBạn có chắc muốn xóa sản phẩm "${productName}"?\n\nHành động này không thể hoàn tác!`);
}

// Search form with animation
const searchForm = document.querySelector('form[action*="search"]');
if (searchForm) {
    const searchInput = searchForm.querySelector('input[name="q"]');
    
    searchInput.addEventListener('focus', function() {
        this.style.transform = 'scale(1.05)';
        this.style.borderColor = '#0D47A1';
    });
    
    searchInput.addEventListener('blur', function() {
        this.style.transform = 'scale(1)';
    });
    
    searchForm.addEventListener('submit', function(e) {
        if (searchInput.value.trim() === '') {
            e.preventDefault();
            searchInput.style.animation = 'shake 0.5s ease';
            setTimeout(() => {
                searchInput.style.animation = '';
                searchInput.focus();
            }, 500);
        }
    });
}

// Password strength indicator
const passwordInput = document.querySelector('input[name="password"]');
if (passwordInput && window.location.pathname.includes('register')) {
    const strengthIndicator = document.createElement('div');
    strengthIndicator.className = 'password-strength';
    strengthIndicator.style.cssText = 'margin-top: 5px; height: 5px; border-radius: 3px; transition: all 0.3s ease;';
    passwordInput.parentElement.appendChild(strengthIndicator);
    
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        let strength = 0;
        
        if (password.length >= 6) strength++;
        if (password.length >= 10) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^A-Za-z0-9]/.test(password)) strength++;
        
        const colors = ['#dc3545', '#ffc107', '#28a745'];
        const widths = ['33%', '66%', '100%'];
        
        if (strength <= 1) {
            strengthIndicator.style.background = colors[0];
            strengthIndicator.style.width = widths[0];
        } else if (strength <= 3) {
            strengthIndicator.style.background = colors[1];
            strengthIndicator.style.width = widths[1];
        } else {
            strengthIndicator.style.background = colors[2];
            strengthIndicator.style.width = widths[2];
        }
    });
}

// Confirm password match indicator
const registerForm = document.querySelector('form[action*="register"]');
if (registerForm) {
    const confirmPassword = registerForm.querySelector('input[name="confirm_password"]');
    
    if (confirmPassword) {
        confirmPassword.addEventListener('input', function() {
            const password = registerForm.querySelector('input[name="password"]').value;
            
            if (this.value === password && this.value.length > 0) {
                this.style.borderColor = '#28a745';
                this.style.background = 'rgba(40, 167, 69, 0.05)';
            } else if (this.value.length > 0) {
                this.style.borderColor = '#dc3545';
                this.style.background = 'rgba(220, 53, 69, 0.05)';
            } else {
                this.style.borderColor = '';
                this.style.background = '';
            }
        });
    }
    
    registerForm.addEventListener('submit', function(e) {
        const password = this.querySelector('input[name="password"]').value;
        const confirmPasswordValue = this.querySelector('input[name="confirm_password"]').value;
        
        if (password !== confirmPasswordValue) {
            e.preventDefault();
            const alert = document.createElement('div');
            alert.className = 'alert alert-danger';
            alert.textContent = '❌ Mật khẩu xác nhận không khớp!';
            this.insertBefore(alert, this.firstChild);
            
            setTimeout(() => alert.remove(), 3000);
        }
    });
}

// Smooth back to top button
const backToTopBtn = document.createElement('button');
backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
backToTopBtn.className = 'btn btn-primary back-to-top';
backToTopBtn.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    display: none;
    z-index: 1000;
    border-radius: 50%;
    width: 55px;
    height: 55px;
    box-shadow: 0 8px 25px rgba(13, 71, 161, 0.4);
    transition: all 0.3s ease;
`;
document.body.appendChild(backToTopBtn);

window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
        backToTopBtn.style.display = 'block';
        backToTopBtn.style.opacity = '1';
    } else {
        backToTopBtn.style.opacity = '0';
        setTimeout(() => {
            if (window.scrollY <= 300) {
                backToTopBtn.style.display = 'none';
            }
        }, 300);
    }
});

backToTopBtn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

backToTopBtn.addEventListener('mouseenter', function() {
    this.style.transform = 'scale(1.1) rotate(360deg)';
});

backToTopBtn.addEventListener('mouseleave', function() {
    this.style.transform = 'scale(1) rotate(0deg)';
});

// Loading animation (chỉ áp dụng cho form không phải checkout)
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form:not([action*="checkout"])');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Đang xử lý...';
            }
        });
    });
});

// Image lazy load with fade effect
document.querySelectorAll('img').forEach(img => {
    img.addEventListener('load', function() {
        this.style.animation = 'fadeIn 0.5s ease';
    });
});

// Add animations CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
        20%, 40%, 60%, 80% { transform: translateX(10px); }
    }
`;
document.head.appendChild(style);

console.log('🚀 SAMSUM Center - Enhanced Flask App loaded successfully!');
console.log('✨ Modern UI with smooth animations ready!');
