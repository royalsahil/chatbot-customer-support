"""
Response Generator
Generates appropriate responses based on detected intent
"""
from database import db
from database.models import FAQCategory

class ResponseGenerator:
    """
    Generates responses for different intents
    Uses database-stored templates and dynamic content
    """
    
    def __init__(self):
        """Initialize response generator with default fallback responses"""
        self.fallback_responses = {
            'unknown': (
                "I'm sorry, I didn't quite understand that. 🤔\n\n"
                "I can help you with:\n"
                "• Order status and tracking\n"
                "• Order cancellation\n"
                "• Refund policy\n"
                "• Product information\n"
                "• Contact support\n\n"
                "Could you please rephrase your question?"
            )
        }
    
    def get_response(self, intent, confidence, entities=None):
        """
        Get response for given intent
        
        Args:
            intent (str): Detected intent
            confidence (float): Confidence score of intent detection
            entities (dict): Extracted entities from user message
        
        Returns:
            str: Generated response
        """
        # If confidence is too low, use fallback
        if confidence < 0.3:
            return self.fallback_responses['unknown']
        
        # Try to get response from database
        try:
            faq = FAQCategory.query.filter_by(
                category=intent,
                is_active=True
            ).first()
            
            if faq:
                response = faq.response_template
                
                # Personalize response with extracted entities
                if entities:
                    response = self._personalize_response(response, entities)
                
                return response
        except Exception as e:
            print(f"Error fetching FAQ response: {e}")
        
        # If no database response, use fallback
        return self.fallback_responses.get(intent, self.fallback_responses['unknown'])
    
    def _personalize_response(self, response, entities):
        """
        Personalize response with extracted entities
        
        Args:
            response (str): Template response
            entities (dict): Extracted entities
        
        Returns:
            str: Personalized response
        """
        # If order_id is present, add it to the response
        if 'order_id' in entities:
            order_id = entities['order_id']
            response += f"\n\n📦 Order ID: {order_id}"
        
        return response
    
    def get_suggested_questions(self, intent):
        """
        Get suggested follow-up questions based on current intent
        
        Args:
            intent (str): Current intent
        
        Returns:
            list: List of suggested questions
        """
        suggestions = {
            'greeting': [
                'Check order status',
                'Cancel my order',
                'Refund policy',
                'Contact support'
            ],
            'order_status': [
                'How to cancel order?',
                'When will it be delivered?',
                'Contact support'
            ],
            'order_cancellation': [
                'Check refund policy',
                'Track my order',
                'Contact support'
            ],
            'refund_policy': [
                'How to return a product?',
                'Contact support',
                'Check order status'
            ],
            'product_info': [
                'Check availability',
                'Compare products',
                'Contact support'
            ],
            'unknown': [
                'Order status',
                'Refund policy',
                'Product information',
                'Contact support'
            ]
        }
        
        return suggestions.get(intent, suggestions['unknown'])
