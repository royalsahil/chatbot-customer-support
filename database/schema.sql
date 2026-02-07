-- Database schema for Customer Support Chatbot
-- This file documents the database structure

-- Table: conversations
-- Stores all chat conversations between users and the bot
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(100) NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    intent VARCHAR(50),
    confidence FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(50),
    feedback VARCHAR(20),
    INDEX idx_session_id (session_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_intent (intent)
);

-- Table: faq_categories
-- Stores FAQ categories and their predefined responses
CREATE TABLE IF NOT EXISTS faq_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(100) UNIQUE NOT NULL,
    response_template TEXT NOT NULL,
    keywords TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category)
);

-- Insert default FAQ responses
INSERT INTO faq_categories (category, response_template, keywords) VALUES
('order_status', 'To check your order status, please visit your account dashboard or enter your order ID. You can track your order in real-time. If you need further assistance, please provide your order number.', 'order,status,track,tracking,where,shipment,delivery'),
('order_cancellation', 'To cancel your order:\n1. Go to "My Orders" section\n2. Select the order you want to cancel\n3. Click "Cancel Order"\n\nNote: Orders can only be cancelled within 24 hours of placement and before shipping. If already shipped, you can initiate a return after delivery.', 'cancel,cancellation,stop,abort,remove order'),
('refund_policy', 'Our refund policy:\n- Refunds are processed within 5-7 business days\n- Original payment method will be credited\n- Product must be in original condition\n- Returns accepted within 30 days\n\nFor damaged/defective items, we offer full refund or replacement.', 'refund,money back,return,exchange,replace'),
('contact_support', 'You can reach our support team:\n📧 Email: support@company.com\n📞 Phone: 1-800-123-4567 (Mon-Fri, 9AM-6PM)\n💬 Live Chat: Available on our website\n\nOur team typically responds within 24 hours.', 'contact,support,help,email,phone,human,agent,representative'),
('product_info', 'I can help you with product information! Please specify:\n- Product name or category\n- Specific details you need (price, features, availability)\n\nYou can also browse our catalog at www.company.com/products', 'product,item,price,cost,available,stock,specification,feature,details'),
('greeting', 'Hello! 👋 Welcome to our Customer Support. I\'m here to help you with:\n- Order status & tracking\n- Order cancellation\n- Refund policy\n- Product information\n- General inquiries\n\nHow can I assist you today?', 'hello,hi,hey,good morning,good evening,greetings'),
('thanks', 'You\'re welcome! 😊 Is there anything else I can help you with?', 'thanks,thank you,appreciate,grateful'),
('goodbye', 'Goodbye! Have a great day! If you need any further assistance, feel free to come back anytime. 👋', 'bye,goodbye,see you,take care,exit');
