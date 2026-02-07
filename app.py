"""
Flask Application - Customer Support Chatbot
Main application file with routes and initialization
"""
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from datetime import datetime
import uuid
import os

# Import configuration
from config import Config

# Import database
from database import db
from database.models import Conversation, FAQCategory

# Import NLP components
from nlp.intent_classifier import IntentClassifier
from nlp.responses import ResponseGenerator

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)  # Enable CORS for API requests
db.init_app(app)  # Initialize database

# Initialize NLP components
intent_classifier = IntentClassifier()
response_generator = ResponseGenerator()


def init_database():
    """Initialize database and create tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if FAQ categories exist, if not, add default ones
        if FAQCategory.query.count() == 0:
            default_faqs = [
                {
                    'category': 'greeting',
                    'response_template': (
                        "Hello! 👋 Welcome to our Customer Support. "
                        "I'm here to help you with:\n"
                        "- Order status & tracking\n"
                        "- Order cancellation\n"
                        "- Refund policy\n"
                        "- Product information\n"
                        "- General inquiries\n\n"
                        "How can I assist you today?"
                    ),
                    'keywords': 'hello,hi,hey,good morning,good evening,greetings'
                },
                {
                    'category': 'order_status',
                    'response_template': (
                        "To check your order status, please visit your account dashboard "
                        "or enter your order ID. You can track your order in real-time. "
                        "If you need further assistance, please provide your order number."
                    ),
                    'keywords': 'order,status,track,tracking,where,shipment,delivery'
                },
                {
                    'category': 'order_cancellation',
                    'response_template': (
                        "To cancel your order:\n"
                        "1. Go to 'My Orders' section\n"
                        "2. Select the order you want to cancel\n"
                        "3. Click 'Cancel Order'\n\n"
                        "Note: Orders can only be cancelled within 24 hours of placement "
                        "and before shipping. If already shipped, you can initiate a "
                        "return after delivery."
                    ),
                    'keywords': 'cancel,cancellation,stop,abort,remove order'
                },
                {
                    'category': 'refund_policy',
                    'response_template': (
                        "Our refund policy:\n"
                        "- Refunds are processed within 5-7 business days\n"
                        "- Original payment method will be credited\n"
                        "- Product must be in original condition\n"
                        "- Returns accepted within 30 days\n\n"
                        "For damaged/defective items, we offer full refund or replacement."
                    ),
                    'keywords': 'refund,money back,return,exchange,replace'
                },
                {
                    'category': 'contact_support',
                    'response_template': (
                        "You can reach our support team:\n"
                        "📧 Email: support@company.com\n"
                        "📞 Phone: 1-800-123-4567 (Mon-Fri, 9AM-6PM)\n"
                        "💬 Live Chat: Available on our website\n\n"
                        "Our team typically responds within 24 hours."
                    ),
                    'keywords': 'contact,support,help,email,phone,human,agent,representative'
                },
                {
                    'category': 'product_info',
                    'response_template': (
                        "I can help you with product information! Please specify:\n"
                        "- Product name or category\n"
                        "- Specific details you need (price, features, availability)\n\n"
                        "You can also browse our catalog at www.company.com/products"
                    ),
                    'keywords': 'product,item,price,cost,available,stock,specification,feature,details'
                },
                {
                    'category': 'thanks',
                    'response_template': (
                        "You're welcome! 😊 Is there anything else I can help you with?"
                    ),
                    'keywords': 'thanks,thank you,appreciate,grateful'
                },
                {
                    'category': 'goodbye',
                    'response_template': (
                        "Goodbye! Have a great day! If you need any further assistance, "
                        "feel free to come back anytime. 👋"
                    ),
                    'keywords': 'bye,goodbye,see you,take care,exit'
                }
            ]
            
            for faq_data in default_faqs:
                faq = FAQCategory(**faq_data)
                db.session.add(faq)
            
            db.session.commit()
            print("✓ Default FAQ categories added to database")


@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')


@app.route('/admin')
def admin():
    """Render the admin panel"""
    return render_template('admin.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Processes user message and returns bot response
    """
    try:
        # Get user message from request
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        # Get or create session ID
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        session_id = session['session_id']
        
        # Classify intent using NLP
        intent, confidence = intent_classifier.classify_intent(user_message)
        
        # Extract entities
        entities = intent_classifier.extract_entities(user_message, intent)
        
        # Generate response
        bot_response = response_generator.get_response(intent, confidence, entities)
        
        # Get suggested questions
        suggestions = response_generator.get_suggested_questions(intent)
        
        # Get user's IP address
        ip_address = request.remote_addr
        
        # Store conversation in database
        conversation = Conversation(
            session_id=session_id,
            user_message=user_message,
            bot_response=bot_response,
            intent=intent,
            confidence=confidence,
            ip_address=ip_address
        )
        db.session.add(conversation)
        db.session.commit()
        
        # Return response
        return jsonify({
            'success': True,
            'response': bot_response,
            'intent': intent,
            'confidence': round(confidence, 2),
            'suggestions': suggestions,
            'conversation_id': conversation.id
        })
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred processing your message'
        }), 500


@app.route('/api/feedback', methods=['POST'])
def feedback():
    """
    Endpoint to receive user feedback on bot responses
    """
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        feedback_value = data.get('feedback')  # 'positive' or 'negative'
        
        if not conversation_id or not feedback_value:
            return jsonify({
                'success': False,
                'error': 'Missing required parameters'
            }), 400
        
        # Update conversation with feedback
        conversation = Conversation.query.get(conversation_id)
        if conversation:
            conversation.feedback = feedback_value
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Thank you for your feedback!'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Conversation not found'
            }), 404
    
    except Exception as e:
        print(f"Error in feedback endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred'
        }), 500


@app.route('/api/admin/conversations', methods=['GET'])
def get_conversations():
    """
    Admin endpoint to get all conversations
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Query conversations with pagination
        conversations = Conversation.query.order_by(
            Conversation.timestamp.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'conversations': [conv.to_dict() for conv in conversations.items],
            'total': conversations.total,
            'pages': conversations.pages,
            'current_page': page
        })
    
    except Exception as e:
        print(f"Error in get_conversations endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred'
        }), 500


@app.route('/api/admin/stats', methods=['GET'])
def get_stats():
    """
    Admin endpoint to get chatbot statistics
    """
    try:
        # Total conversations
        total_conversations = Conversation.query.count()
        
        # Conversations by intent
        from sqlalchemy import func
        intent_stats = db.session.query(
            Conversation.intent,
            func.count(Conversation.id).label('count')
        ).group_by(Conversation.intent).all()
        
        # Average confidence by intent
        confidence_stats = db.session.query(
            Conversation.intent,
            func.avg(Conversation.confidence).label('avg_confidence')
        ).group_by(Conversation.intent).all()
        
        # Feedback stats
        positive_feedback = Conversation.query.filter_by(feedback='positive').count()
        negative_feedback = Conversation.query.filter_by(feedback='negative').count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_conversations': total_conversations,
                'intent_distribution': {
                    intent: count for intent, count in intent_stats
                },
                'average_confidence': {
                    intent: round(avg_conf, 2) 
                    for intent, avg_conf in confidence_stats if avg_conf
                },
                'feedback': {
                    'positive': positive_feedback,
                    'negative': negative_feedback
                }
            }
        })
    
    except Exception as e:
        print(f"Error in get_stats endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred'
        }), 500


if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Run the application
    print("=" * 50)
    print("🤖 Customer Support Chatbot Starting...")
    print("=" * 50)
    print("📍 Server running at: http://0.0.0.0:8080")
    print("💬 Chat Interface: http://0.0.0.0:8080")
    print("⚙️  Admin Panel: http://0.0.0.0:8080/admin")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8080)
