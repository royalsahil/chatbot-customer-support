"""
Database models for chatbot application
Defines the schema for storing chat conversations
"""
from datetime import datetime
from database import db

class Conversation(db.Model):
    """
    Model to store user conversations with the chatbot
    Each message (user query and bot response) is stored as a record
    """
    __tablename__ = 'conversations'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Session identifier to group related messages
    session_id = db.Column(db.String(100), nullable=False, index=True)
    
    # User's message
    user_message = db.Column(db.Text, nullable=False)
    
    # Bot's response
    bot_response = db.Column(db.Text, nullable=False)
    
    # Detected intent from NLP processing
    intent = db.Column(db.String(50), nullable=True)
    
    # Confidence score of intent detection (0.0 to 1.0)
    confidence = db.Column(db.Float, nullable=True)
    
    # Timestamp of the conversation
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # User's IP address (optional, for analytics)
    ip_address = db.Column(db.String(50), nullable=True)
    
    # User feedback (optional: positive/negative/none)
    feedback = db.Column(db.String(20), nullable=True)
    
    def __repr__(self):
        return f'<Conversation {self.id}: {self.intent}>'
    
    def to_dict(self):
        """Convert conversation to dictionary for JSON responses"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'intent': self.intent,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat(),
            'feedback': self.feedback
        }


class FAQCategory(db.Model):
    """
    Model to store FAQ categories and their responses
    Allows admin to manage predefined responses
    """
    __tablename__ = 'faq_categories'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Category/Intent name
    category = db.Column(db.String(100), nullable=False, unique=True)
    
    # Response template for this category
    response_template = db.Column(db.Text, nullable=False)
    
    # Keywords associated with this category
    keywords = db.Column(db.Text, nullable=True)  # Comma-separated keywords
    
    # Is this category active?
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamp when created/updated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<FAQCategory {self.category}>'
    
    def to_dict(self):
        """Convert FAQ category to dictionary"""
        return {
            'id': self.id,
            'category': self.category,
            'response_template': self.response_template,
            'keywords': self.keywords,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
