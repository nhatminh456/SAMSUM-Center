// Sales Chatbot Logic (upgraded)
const chatbot = {
    products: [],
    context: {
        budget: null,
        need: null,
    },

    fallbackCatalog: [
        { name: 'Galaxy A05', price: 3490000, series: 'A', tags: ['gia re', 'co ban', 'hoc tap'] },
        { name: 'Galaxy A14', price: 4490000, series: 'A', tags: ['gia re', 'pin tot'] },
        { name: 'Galaxy A25', price: 6290000, series: 'A', tags: ['gia re', 'camera'] },
        { name: 'Galaxy A35', price: 8490000, series: 'A', tags: ['can bang', 'camera', 'man hinh'] },
        { name: 'Galaxy S24', price: 22990000, series: 'S', tags: ['flagship', 'camera', 'hieu nang'] },
        { name: 'Galaxy S24+', price: 27990000, series: 'S', tags: ['flagship', 'pin', 'man hinh'] },
        { name: 'Galaxy S24 Ultra', price: 29990000, series: 'S', tags: ['camera', 'spen', 'flagship'] },
        { name: 'Galaxy S25', price: 24990000, series: 'S', tags: ['flagship', 'hieu nang'] },
        { name: 'Galaxy S25+', price: 29990000, series: 'S', tags: ['flagship', 'pin', 'man hinh'] },
        { name: 'Galaxy S25 Ultra', price: 33990000, series: 'S', tags: ['camera', 'spen', 'flagship'] },
        { name: 'Galaxy Z Flip6', price: 26990000, series: 'Z', tags: ['gap', 'thoi trang', 'nho gon'] },
        { name: 'Galaxy Z Fold6', price: 43990000, series: 'Z', tags: ['gap', 'da nhiem', 'cao cap'] },
        { name: 'Galaxy Z Fold7', price: 44990000, series: 'Z', tags: ['gap', 'da nhiem', 'cao cap'] },
    ],

    init() {
        this.loadProducts();
        this.setupEventListeners();
        this.addBotMessage(
            'Xin chao! Toi la tro ly tu van ban hang cua SAMSUM Center.\n' +
            'Ban co the hoi: ngan sach, nhu cau (choi game/chup anh/lam viec), so sanh may, bao hanh, giao hang.',
            'starter'
        );
    },

    loadProducts() {
        const cards = document.querySelectorAll('.product-card');
        cards.forEach((card) => {
            const nameText = card.querySelector('.card-title, .product-name')?.textContent?.trim() || '';
            const priceText = card.querySelector('.text-danger, .product-price')?.textContent || '';
            const link = card.querySelector('a[href*="/product/"]')?.getAttribute('href') || '';
            const price = this.parsePrice(priceText);

            if (nameText && price > 0) {
                this.products.push({
                    name: nameText,
                    price,
                    series: this.detectSeries(nameText),
                    tags: this.detectTags(nameText),
                    link,
                });
            }
        });

        // Fallback if current page does not expose product cards
        if (!this.products.length) {
            this.products = [...this.fallbackCatalog];
        }
    },

    setupEventListeners() {
        const chatbotBtn = document.getElementById('chatbot-btn');
        const chatbotWindow = document.getElementById('chatbot-window');
        const chatbotClose = document.getElementById('chatbot-close');
        const chatbotSend = document.getElementById('chatbot-send');
        const chatbotInput = document.getElementById('chatbot-input');

        chatbotBtn?.addEventListener('click', () => {
            chatbotWindow?.classList.toggle('active');
            if (chatbotWindow?.classList.contains('active')) {
                chatbotInput?.focus();
            }
        });

        chatbotClose?.addEventListener('click', () => {
            chatbotWindow?.classList.remove('active');
        });

        chatbotSend?.addEventListener('click', () => this.sendMessage());

        chatbotInput?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    },

    sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = (input?.value || '').trim();
        if (!message) return;

        this.addUserMessage(message);
        input.value = '';

        this.showTyping();
        setTimeout(() => {
            this.hideTyping();
            this.processMessage(message);
        }, 600);
    },

    processMessage(message) {
        const text = this.normalize(message);

        const budget = this.extractBudget(text);
        if (budget) {
            this.context.budget = budget;
        }

        const need = this.extractNeed(text);
        if (need) {
            this.context.need = need;
        }

        if (this.isGreeting(text)) {
            this.addBotMessage(
                'Chao ban! Minh se tu van theo nhu cau that.\n' +
                'Ban co the noi kieu: "duoi 10 trieu" hoac "can may chup anh dep".',
                'starter'
            );
            return;
        }

        if (this.isThanks(text)) {
            this.addBotMessage('Rat vui duoc ho tro ban. Neu can, minh co the goi y them 2-3 may theo ngan sach hien tai.');
            return;
        }

        if (this.isWarrantyIntent(text)) {
            this.addBotMessage(
                'Chinh sach tai shop:\n' +
                '- Bao hanh chinh hang 12 thang\n' +
                '- Ho tro doi tra neu loi nha san xuat\n' +
                '- Ho tro ky thuat trong suot qua trinh su dung'
            );
            return;
        }

        if (this.isDeliveryIntent(text)) {
            this.addBotMessage(
                'Thong tin giao hang va thanh toan:\n' +
                '- Co COD, chuyen khoan\n' +
                '- Giao hang toan quoc\n' +
                '- Co the dat truc tiep tren website'
            );
            return;
        }

        if (this.isCompareIntent(text)) {
            this.replyCompare(text);
            return;
        }

        if (this.isPriceIntent(text)) {
            this.replyPrice(text);
            return;
        }

        if (this.isRecommendationIntent(text) || this.context.budget || this.context.need) {
            this.replyRecommendation();
            return;
        }

        this.addBotMessage(
            'Minh co the ho tro nhanh theo 4 kieu:\n' +
            '1) Ngan sach: "duoi 10 trieu"\n' +
            '2) Nhu cau: "choi game", "chup anh", "lam viec"\n' +
            '3) So sanh: "so sanh S24 va S25"\n' +
            '4) Gia 1 dong may: "gia S25 Ultra"',
            'starter'
        );
    },

    replyPrice(text) {
        const candidates = this.findByText(text);
        if (!candidates.length) {
            this.addBotMessage(
                'Minh chua bat duoc mau cu the. Ban co the hoi nhu:\n' +
                '- gia s25 ultra\n' +
                '- gia z flip\n' +
                '- bang gia samsung'
            );
            return;
        }

        const lines = candidates.slice(0, 6).map((p) => `- ${p.name}: ${this.formatCurrency(p.price)}`);
        this.addBotMessage(`Gia tham khao:\n${lines.join('\n')}`);
    },

    replyCompare(text) {
        const targets = this.findByText(text).slice(0, 2);
        if (targets.length < 2) {
            this.addBotMessage(
                'Ban hay chi ro 2 mau de so sanh, vi du:\n' +
                '- so sanh s24 va s25\n' +
                '- so sanh flip6 va fold6'
            );
            return;
        }

        const [a, b] = targets;
        const diff = a.price - b.price;
        const diffLine = diff === 0
            ? 'Hai may co muc gia tuong duong.'
            : `${a.name} ${diff > 0 ? 'cao hon' : 'thap hon'} ${Math.abs(diff).toLocaleString('vi-VN')} VND so voi ${b.name}.`;

        const tip = this.compareTip(a, b);
        this.addBotMessage(
            `So sanh nhanh:\n` +
            `- ${a.name}: ${this.formatCurrency(a.price)}\n` +
            `- ${b.name}: ${this.formatCurrency(b.price)}\n` +
            `- ${diffLine}\n` +
            `- Goi y: ${tip}`
        );
    },

    replyRecommendation() {
        const picks = this.rankProducts(this.context.budget, this.context.need).slice(0, 3);

        if (!picks.length) {
            this.addBotMessage('Minh chua tim thay mau phu hop. Ban thu noi ro hon ve muc gia du kien nhe.');
            return;
        }

        const reasonNeed = this.context.need ? `Nhu cau uu tien: ${this.context.need}.\n` : '';
        const reasonBudget = this.context.budget ? `Ngan sach tham chieu: toi da ${this.formatCurrency(this.context.budget.max)}.\n` : '';

        const lines = picks.map((p, i) => `${i + 1}. ${p.name} - ${this.formatCurrency(p.price)} (${this.reasonFor(p)})`);

        this.addBotMessage(
            `Goi y cho ban:\n${reasonBudget}${reasonNeed}${lines.join('\n')}\n\n` +
            `Neu ban muon, minh co the loc tiep theo tieu chi pin/camera/hieu nang.`
        );
    },

    rankProducts(budget, need) {
        return [...this.products]
            .filter((p) => {
                if (!budget) return true;
                return p.price >= budget.min && p.price <= budget.max;
            })
            .map((p) => ({ ...p, score: this.scoreProduct(p, need) }))
            .sort((a, b) => b.score - a.score || a.price - b.price);
    },

    scoreProduct(product, need) {
        let score = 0;

        if (product.series === 'S') score += 8;
        if (product.series === 'Z') score += 7;
        if (product.series === 'A') score += 5;

        if (!need) return score;

        const tags = product.tags.join(' ');
        if (need === 'game' && (tags.includes('hieu nang') || product.series === 'S')) score += 6;
        if (need === 'camera' && tags.includes('camera')) score += 7;
        if (need === 'work' && (product.series === 'Z' || tags.includes('da nhiem'))) score += 7;
        if (need === 'budget' && product.series === 'A') score += 8;

        return score;
    },

    compareTip(a, b) {
        if (a.series === 'Z' || b.series === 'Z') {
            return 'Dong Z hop voi nguoi uu tien trai nghiem gap va da nhiem.';
        }
        if (a.series === 'A' || b.series === 'A') {
            return 'Dong A toi uu chi phi, dong S/Z manh hon ve camera va hieu nang.';
        }
        return 'Neu can hieu nang va camera tot hon thi uu tien ban Ultra/Plus.';
    },

    reasonFor(product) {
        if (product.series === 'A') return 'toi uu chi phi';
        if (product.series === 'S') return 'flagship can bang';
        if (product.series === 'Z') return 'trai nghiem gap cao cap';
        return 'phu hop da nhu cau';
    },

    isGreeting(text) {
        return /^(xin chao|chao|hello|hi|hey)/.test(text);
    },

    isThanks(text) {
        return /(cam on|thanks|thank you)/.test(text);
    },

    isPriceIntent(text) {
        return /(gia|bao nhieu|muc gia|bang gia)/.test(text);
    },

    isRecommendationIntent(text) {
        return /(tu van|nen mua|goi y|de xuat|chon may|chon gi)/.test(text);
    },

    isCompareIntent(text) {
        return /(so sanh|khac nhau|vs\b|voi\b)/.test(text);
    },

    isWarrantyIntent(text) {
        return /(bao hanh|doi tra|ho tro ky thuat)/.test(text);
    },

    isDeliveryIntent(text) {
        return /(giao hang|ship|thanh toan|cod|van chuyen)/.test(text);
    },

    extractNeed(text) {
        if (/(choi game|gaming|hieu nang|fps)/.test(text)) return 'game';
        if (/(chup anh|camera|quay phim|selfie)/.test(text)) return 'camera';
        if (/(lam viec|da nhiem|office|van phong)/.test(text)) return 'work';
        if (/(gia re|tiet kiem|hoc sinh|sinh vien|budget)/.test(text)) return 'budget';
        return null;
    },

    extractBudget(text) {
        const clean = text.replace(/\./g, '').replace(/,/g, '');

        // Format: "duoi 10 trieu"
        let m = clean.match(/(duoi|toi da|khong qua)\s*(\d+)\s*(trieu|m|k)?/);
        if (m) {
            const value = this.toVnd(Number(m[2]), m[3]);
            return { min: 0, max: value };
        }

        // Format: "tu 10 den 15 trieu" or "10-15 trieu"
        m = clean.match(/(tu\s*)?(\d+)\s*(trieu|m|k)?\s*(den|-|toi)\s*(\d+)\s*(trieu|m|k)?/);
        if (m) {
            const min = this.toVnd(Number(m[2]), m[3]);
            const max = this.toVnd(Number(m[5]), m[6]);
            return { min: Math.min(min, max), max: Math.max(min, max) };
        }

        // Format: "20 trieu"
        m = clean.match(/\b(\d+)\s*(trieu|m|k)\b/);
        if (m) {
            const value = this.toVnd(Number(m[1]), m[2]);
            return { min: Math.floor(value * 0.8), max: value };
        }

        return null;
    },

    toVnd(value, unit) {
        if (!unit || unit === 'trieu' || unit === 'm') return value * 1000000;
        if (unit === 'k') return value * 1000;
        return value;
    },

    findByText(text) {
        const normalized = this.normalize(text);

        // Try exact name hits first
        const byName = this.products.filter((p) => normalized.includes(this.normalize(p.name)));
        if (byName.length) return byName;

        // Series/group level hits
        const out = [];
        if (/(s24|galaxy s24)/.test(normalized)) out.push(...this.products.filter((p) => /s24/i.test(p.name)));
        if (/(s25|galaxy s25)/.test(normalized)) out.push(...this.products.filter((p) => /s25/i.test(p.name)));
        if (/ultra/.test(normalized)) out.push(...this.products.filter((p) => /ultra/i.test(p.name)));
        if (/flip/.test(normalized)) out.push(...this.products.filter((p) => /flip/i.test(p.name)));
        if (/fold|gap/.test(normalized)) out.push(...this.products.filter((p) => /fold/i.test(p.name)));
        if (/a\d\d|a series|dong a/.test(normalized)) out.push(...this.products.filter((p) => p.series === 'A'));

        // Deduplicate by name
        const seen = new Set();
        return out.filter((p) => {
            const key = p.name.toLowerCase();
            if (seen.has(key)) return false;
            seen.add(key);
            return true;
        });
    },

    detectSeries(name) {
        const n = name.toLowerCase();
        if (n.includes('fold') || n.includes('flip') || /\bz\b/.test(n)) return 'Z';
        if (/\bs\d+/i.test(name) || n.includes('galaxy s')) return 'S';
        if (/\ba\d+/i.test(name) || n.includes('galaxy a')) return 'A';
        return 'O';
    },

    detectTags(name) {
        const n = name.toLowerCase();
        const tags = [];
        if (n.includes('ultra')) tags.push('camera', 'hieu nang');
        if (n.includes('fold')) tags.push('da nhiem', 'cao cap');
        if (n.includes('flip')) tags.push('thoi trang', 'nho gon');
        if (/\ba\d+/i.test(name)) tags.push('gia re');
        if (/\bs\d+/i.test(name)) tags.push('flagship', 'hieu nang');
        return tags;
    },

    parsePrice(text) {
        const digits = (text || '').replace(/[^0-9]/g, '');
        return digits ? Number(digits) : 0;
    },

    formatCurrency(price) {
        return `${Number(price || 0).toLocaleString('vi-VN')} VND`;
    },

    normalize(text) {
        return (text || '')
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/đ/g, 'd')
            .trim();
    },

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        };
        return String(text).replace(/[&<>"']/g, (m) => map[m]);
    },

    addUserMessage(text) {
        const messagesDiv = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';
        messageDiv.innerHTML = `<div class="message-content">${this.escapeHtml(text)}</div>`;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    },

    addBotMessage(text, quickType = null) {
        const messagesDiv = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';

        let html = `<div class="message-content">${this.escapeHtml(text).replace(/\n/g, '<br>')}</div>`;
        if (quickType) {
            html += this.renderQuickReplies(quickType);
        }

        messageDiv.innerHTML = html;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    },

    renderQuickReplies(type) {
        if (type !== 'starter') return '';

        return `
            <div class="quick-replies">
                <button class="quick-reply-btn" onclick="chatbot.handleQuickReply('duoi 10 trieu')">Duoi 10 trieu</button>
                <button class="quick-reply-btn" onclick="chatbot.handleQuickReply('can may chup anh dep')">Chup anh dep</button>
                <button class="quick-reply-btn" onclick="chatbot.handleQuickReply('so sanh s24 va s25')">So sanh S24 va S25</button>
            </div>
        `;
    },

    handleQuickReply(text) {
        const input = document.getElementById('chatbot-input');
        if (!input) return;
        input.value = text;
        this.sendMessage();
    },

    showTyping() {
        const messagesDiv = document.getElementById('chatbot-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        `;
        messagesDiv.appendChild(typingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    },

    hideTyping() {
        const typingDiv = document.getElementById('typing-indicator');
        if (typingDiv) typingDiv.remove();
    }
};

document.addEventListener('DOMContentLoaded', () => {
    chatbot.init();
});
