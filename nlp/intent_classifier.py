"""
Intent Classifier using NLTK
Processes user input and determines the intent using NLP techniques
"""
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data (will be done in app initialization)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
    
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

# punkt_tab is included in punkt package
# No need to download separately


class IntentClassifier:
    """
    NLP-based intent classifier for customer support chatbot
    Uses NLTK for text preprocessing and intent matching
    """
    
    def __init__(self):
        """Initialize the classifier with predefined intents and patterns"""
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Define intent patterns with keywords and phrases
        # Each intent has associated keywords and their weights
        self.intents = {
            'greeting': {
                'keywords': ['hello', 'hi', 'hey', 'good', 'morning', 'evening', 'greetings'],
                'phrases': ['good morning', 'good evening', 'good afternoon'],
                'weight': 1.0
            },
            'order_status': {
                'keywords': ['order', 'status', 'track', 'tracking', 'where', 'shipment', 
                           'delivery', 'package', 'shipping', 'delivered', 'location'],
                'phrases': ['order status', 'track order', 'where is my order', 
                          'check order', 'order tracking'],
                'weight': 1.2
            },
            'order_cancellation': {
                'keywords': ['cancel', 'cancellation', 'stop', 'abort', 'remove', 
                           'delete', 'undo', 'withdraw'],
                'phrases': ['cancel order', 'cancel my order', 'stop order', 
                          'remove order', 'cancel shipment'],
                'weight': 1.2
            },
            'refund_policy': {
                'keywords': ['refund', 'money', 'back', 'return', 'exchange', 
                           'replace', 'replacement', 'policy', 'reimbursement'],
                'phrases': ['refund policy', 'money back', 'return policy', 
                          'get refund', 'request refund'],
                'weight': 1.2
            },
            'contact_support': {
                'keywords': ['contact', 'support', 'help', 'email', 'phone', 
                           'human', 'agent', 'representative', 'talk', 'speak', 'call'],
                'phrases': ['contact support', 'talk to human', 'speak to agent', 
                          'customer service', 'reach support'],
                'weight': 1.1
            },
            'product_info': {
                'keywords': ['product', 'item', 'price', 'cost', 'available', 
                           'stock', 'specification', 'feature', 'details', 'information'],
                'phrases': ['product information', 'product details', 'item price', 
                          'check price', 'product availability'],
                'weight': 1.0
            },
            'thanks': {
                'keywords': ['thanks', 'thank', 'appreciate', 'grateful', 'awesome'],
                'phrases': ['thank you', 'thanks a lot', 'appreciate it'],
                'weight': 1.0
            },
            'goodbye': {
                'keywords': ['bye', 'goodbye', 'exit', 'quit', 'close', 'leave'],
                'phrases': ['see you', 'take care', 'talk later', 'good bye'],
                'weight': 1.0
            }
        }
    
    def preprocess_text(self, text):
        """
        Preprocess the input text
        - Convert to lowercase
        - Remove special characters
        - Tokenize
        - Remove stopwords (selective)
        - Lemmatize
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords (but keep important ones for context)
        important_words = {'not', 'no', 'where', 'when', 'how', 'can', 'my'}
        filtered_tokens = [
            token for token in tokens 
            if token not in self.stop_words or token in important_words
        ]
        
        # Lemmatize
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in filtered_tokens]
        
        return {
            'original': text,
            'tokens': lemmatized_tokens,
            'text': ' '.join(lemmatized_tokens)
        }
    
    def calculate_intent_score(self, processed_text, intent_data):
        """
        Calculate similarity score between processed text and intent
        Uses keyword matching and phrase matching with weights
        """
        score = 0.0
        tokens = processed_text['tokens']
        text = processed_text['text']
        
        # Check for phrase matches (higher weight)
        for phrase in intent_data['phrases']:
            if phrase in processed_text['original']:
                score += 2.0 * intent_data['weight']
        
        # Check for keyword matches
        for keyword in intent_data['keywords']:
            if keyword in tokens:
                score += 1.0 * intent_data['weight']
        
        # Normalize score by number of tokens (avoid bias toward longer texts)
        if len(tokens) > 0:
            score = score / (len(tokens) ** 0.5)
        
        return score
    
    def classify_intent(self, user_message):
        """
        Classify the intent of user message
        Returns intent name and confidence score
        """
        # Preprocess the message
        processed = self.preprocess_text(user_message)
        
        # Calculate scores for all intents
        intent_scores = {}
        for intent_name, intent_data in self.intents.items():
            score = self.calculate_intent_score(processed, intent_data)
            intent_scores[intent_name] = score
        
        # Get the intent with highest score
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            best_score = intent_scores[best_intent]
            
            # Set confidence threshold
            # If score is too low, classify as unknown
            if best_score < 0.5:
                return 'unknown', 0.0
            
            # Normalize confidence to 0-1 range
            confidence = min(best_score / 3.0, 1.0)
            
            return best_intent, confidence
        
        return 'unknown', 0.0
    
    def extract_entities(self, user_message, intent):
        """
        Extract entities from user message based on intent
        For example, extract order ID for order-related queries
        """
        entities = {}
        
        # Extract order ID pattern (e.g., ORD12345, #12345, etc.)
        if intent in ['order_status', 'order_cancellation']:
            order_pattern = r'(?:order\s*(?:id|number|#)?\s*[:=]?\s*)?([A-Z]*\d{4,})'
            matches = re.findall(order_pattern, user_message, re.IGNORECASE)
            if matches:
                entities['order_id'] = matches[0]
        
        return entities
