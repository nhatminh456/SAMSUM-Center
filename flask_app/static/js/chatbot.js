// Chatbot Logic
const chatbot = {
    products: [],
    
    init() {
        this.loadProducts();
        this.setupEventListeners();
        this.addBotMessage("Xin chào! 👋 Tôi là trợ lý ảo của SAMSUNG Center. Tôi có thể giúp gì cho bạn?", true);
    },
    
    loadProducts() {
        // Load products from page if available
        const productElements = document.querySelectorAll('.product-card');
        productElements.forEach(el => {
            const id = el.getAttribute('data-id');
            const name = el.querySelector('.product-name')?.textContent;
            const price = el.querySelector('.product-price')?.textContent;
            if (id && name && price) {
                this.products.push({ id, name, price });
            }
        });
    },
    
    setupEventListeners() {
        const chatbotBtn = document.getElementById('chatbot-btn');
        const chatbotWindow = document.getElementById('chatbot-window');
        const chatbotClose = document.getElementById('chatbot-close');
        const chatbotSend = document.getElementById('chatbot-send');
        const chatbotInput = document.getElementById('chatbot-input');
        
        chatbotBtn.addEventListener('click', () => {
            chatbotWindow.classList.toggle('active');
            if (chatbotWindow.classList.contains('active')) {
                chatbotInput.focus();
            }
        });
        
        chatbotClose.addEventListener('click', () => {
            chatbotWindow.classList.remove('active');
        });
        
        chatbotSend.addEventListener('click', () => this.sendMessage());
        
        chatbotInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    },
    
    sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        this.addUserMessage(message);
        input.value = '';
        
        // Show typing indicator
        this.showTyping();
        
        // Process message and respond
        setTimeout(() => {
            this.hideTyping();
            this.processMessage(message);
        }, 1000);
    },
    
    processMessage(message) {
        const lowerMsg = message.toLowerCase();
        
        // Greetings
        if (lowerMsg.match(/^(xin chào|chào|hello|hi|hey)/)) {
            this.addBotMessage("Xin chào! Tôi có thể giúp bạn tìm sản phẩm Samsung phù hợp. Bạn đang quan tâm đến sản phẩm nào?", true);
            return;
        }
        
        // Price inquiry
        if (lowerMsg.includes('giá') || lowerMsg.includes('bao nhiêu')) {
            if (lowerMsg.includes('s24') || lowerMsg.includes('galaxy s24')) {
                this.addBotMessage("Samsung Galaxy S24 có các phiên bản:\n• S24: 22.990.000₫\n• S24+: 27.990.000₫\n• S24 Ultra: 29.990.000₫\n\nBạn muốn xem chi tiết sản phẩm nào?");
            } else if (lowerMsg.includes('s25') || lowerMsg.includes('galaxy s25')) {
                this.addBotMessage("Samsung Galaxy S25 có các phiên bản:\n• S25: 24.990.000₫\n• S25+: 29.990.000₫\n• S25 Ultra: 33.990.000₫\n\nĐây là dòng flagship mới nhất!");
            } else if (lowerMsg.includes('fold') || lowerMsg.includes('gập')) {
                this.addBotMessage("Samsung Galaxy Z Fold có các phiên bản:\n• Z Fold5: 41.990.000₫\n• Z Fold6: 43.990.000₫\n• Z Fold7: 44.990.000₫\n\nĐiện thoại gập cao cấp nhất!");
            } else if (lowerMsg.includes('flip')) {
                this.addBotMessage("Samsung Galaxy Z Flip có các phiên bản:\n• Z Flip4: 23.990.000₫\n• Z Flip5: 25.990.000₫\n• Z Flip6: 26.990.000₫\n• Z Flip7: 28.990.000₫");
            } else {
                this.addBotMessage("Bạn muốn hỏi giá sản phẩm nào? Chúng tôi có:\n• Galaxy S Series (S24, S25)\n• Galaxy Z Fold (gập dọc)\n• Galaxy Z Flip (gập ngang)\n• Galaxy A Series\n• Phụ kiện");
            }
            return;
        }
        
        // Product recommendations
        if (lowerMsg.includes('tư vấn') || lowerMsg.includes('nên mua') || lowerMsg.includes('đề xuất')) {
            if (lowerMsg.includes('rẻ') || lowerMsg.includes('tiết kiệm') || lowerMsg.includes('budget')) {
                this.addBotMessage("Với ngân sách tiết kiệm, tôi đề xuất:\n\n📱 Galaxy A Series:\n• A05: 3.490.000₫\n• A14: 4.490.000₫\n• A25: 6.290.000₫\n• A35: 8.490.000₫\n\nCác dòng A vẫn đảm bảo chất lượng Samsung với giá phải chăng!");
            } else if (lowerMsg.includes('cao cấp') || lowerMsg.includes('flagship') || lowerMsg.includes('tốt nhất')) {
                this.addBotMessage("Dòng cao cấp nhất hiện tại:\n\n🌟 Galaxy S25 Ultra: 33.990.000₫\n• Chip Snapdragon 8 Gen 3\n• Camera 200MP\n• Bút S-Pen tích hợp\n• Pin 5000mAh\n\n📱 Galaxy Z Fold7: 44.990.000₫\n• Màn hình gập độc đáo\n• Đa nhiệm tuyệt vời\n• Trải nghiệm tablet/điện thoại 2 trong 1");
            } else if (lowerMsg.includes('chụp ảnh') || lowerMsg.includes('camera')) {
                this.addBotMessage("Để chụp ảnh đẹp, tôi đề xuất:\n\n📸 S25 Ultra - Camera 200MP\n📸 S24 Ultra - Camera 200MP\n📸 S23 Ultra - Camera 200MP\n\nCả 3 đều có hệ thống camera xuất sắc với AI xử lý ảnh thông minh!");
            } else {
                this.addBotMessage("Để tư vấn chính xác, bạn cho tôi biết:\n\n1️⃣ Ngân sách dự kiến?\n2️⃣ Nhu cầu sử dụng chính (chơi game, chụp ảnh, làm việc)?\n3️⃣ Có thích màn hình gập không?");
            }
            return;
        }
        
        // Compare products
        if (lowerMsg.includes('so sánh') || lowerMsg.includes('khác nhau')) {
            this.addBotMessage("Bạn muốn so sánh sản phẩm nào?\n\nVí dụ: 'So sánh S24 và S25' hoặc 'Khác nhau giữa Fold và Flip'");
            return;
        }
        
        // Warranty & Support
        if (lowerMsg.includes('bảo hành') || lowerMsg.includes('đổi trả')) {
            this.addBotMessage("📋 Chính sách bảo hành:\n\n✅ Bảo hành chính hãng 12 tháng\n✅ Đổi trả trong 7 ngày nếu có lỗi\n✅ Hỗ trợ kỹ thuật 24/7\n✅ Bảo hành tận nơi\n\nBạn cần thông tin gì cụ thể hơn?");
            return;
        }
        
        // Payment & Delivery
        if (lowerMsg.includes('thanh toán') || lowerMsg.includes('giao hàng') || lowerMsg.includes('ship')) {
            this.addBotMessage("💳 Thanh toán & Giao hàng:\n\n✅ COD (Thanh toán khi nhận hàng)\n✅ Chuyển khoản ngân hàng\n✅ Ví điện tử (MoMo, ZaloPay)\n✅ Miễn phí vận chuyển toàn quốc\n✅ Giao hàng trong 2-3 ngày\n\nBạn có thể đặt hàng ngay trên website!");
            return;
        }
        
        // Contact
        if (lowerMsg.includes('liên hệ') || lowerMsg.includes('hotline') || lowerMsg.includes('địa chỉ')) {
            this.addBotMessage("📞 Thông tin liên hệ:\n\n• Hotline: 1900-xxxx\n• Email: support@samsumcenter.vn\n• Địa chỉ: [Địa chỉ cửa hàng]\n• Giờ làm việc: 8h-22h hàng ngày\n\nBạn có thể liên hệ bất cứ lúc nào!");
            return;
        }
        
        // Default response
        this.addBotMessage("Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể hỏi tôi về:\n\n💰 Giá sản phẩm\n📱 Tư vấn mua hàng\n🔄 So sánh sản phẩm\n🛡️ Bảo hành\n🚚 Giao hàng & thanh toán\n📞 Liên hệ", true);
    },
    
    addUserMessage(text) {
        const messagesDiv = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';
        messageDiv.innerHTML = `<div class="message-content">${text}</div>`;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    },
    
    addBotMessage(text, showQuickReplies = false) {
        const messagesDiv = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        
        let html = `<div class="message-content">${text.replace(/\n/g, '<br>')}</div>`;
        
        if (showQuickReplies) {
            html += `
                <div class="quick-replies">
                    <button class="quick-reply-btn" onclick="chatbot.handleQuickReply('Giá sản phẩm')">Giá sản phẩm</button>
                    <button class="quick-reply-btn" onclick="chatbot.handleQuickReply('Tư vấn mua hàng')">Tư vấn mua hàng</button>
                    <button class="quick-reply-btn" onclick="chatbot.handleQuickReply('Bảo hành')">Bảo hành</button>
                </div>
            `;
        }
        
        messageDiv.innerHTML = html;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    },
    
    handleQuickReply(text) {
        document.getElementById('chatbot-input').value = text;
        this.sendMessage();
    },
    
    showTyping() {
        const messagesDiv = document.getElementById('chatbot-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        messagesDiv.appendChild(typingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    },
    
    hideTyping() {
        const typingDiv = document.getElementById('typing-indicator');
        if (typingDiv) {
            typingDiv.remove();
        }
    }
};

// Initialize chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    chatbot.init();
});
