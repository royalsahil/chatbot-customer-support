# 🤖 Customer Support Chatbot

A complete web-based intelligent chatbot for customer support built with Python Flask, featuring Natural Language Processing (NLP) using NLTK for intent recognition and automatic response generation.

## 📋 Features

### Core Functionality
- ✅ **Real-time Chat Interface** - Clean, modern, and responsive UI
- ✅ **Natural Language Processing** - Uses NLTK for intent classification
- ✅ **Smart Intent Recognition** - Understands user queries beyond simple keyword matching
- ✅ **Entity Extraction** - Extracts order IDs and other relevant information
- ✅ **Database Storage** - Stores all conversations for analytics
- ✅ **Admin Dashboard** - View conversations, statistics, and analytics
- ✅ **Suggested Questions** - Context-aware quick replies
- ✅ **Typing Indicators** - Professional chat experience
- ✅ **Conversation History** - Persistent chat using localStorage

### Supported Intents
1. **Order Status** - Track and check order status
2. **Order Cancellation** - Cancel orders and shipments
3. **Refund Policy** - Information about refunds and returns
4. **Contact Support** - Get human support contact details
5. **Product Information** - Query about products and pricing
6. **Greetings & Farewells** - Natural conversation flow
7. **Thanks** - Acknowledge user gratitude

## 🏗️ Project Structure

```
CHATBOT FOR CUSTOMER SUPPORT/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── database/                   # Database module
│   ├── __init__.py            # Database initialization
│   ├── models.py              # SQLAlchemy models
│   └── schema.sql             # Database schema documentation
│
├── nlp/                       # NLP module
│   ├── __init__.py           
│   ├── intent_classifier.py  # NLTK-based intent classifier
│   └── responses.py           # Response generator
│
├── static/                    # Static files
│   ├── css/
│   │   └── style.css         # Main stylesheet
│   └── js/
│       └── chat.js           # Frontend JavaScript
│
└── templates/                 # HTML templates
    ├── index.html            # Chat interface
    └── admin.html            # Admin dashboard
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd "/Volumes/MY SSD/APPS/CHATBOT FOR CUSTOMER SUPPORT"

# Install required packages
pip install -r requirements.txt
```

### Step 2: Download NLTK Data

The application will automatically download required NLTK data on first run, but you can pre-download it:

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

### Step 3: Initialize Database

The database will be created automatically when you first run the application. It uses SQLite by default.

### Step 4: Run the Application

```bash
python app.py
```

The server will start at: **http://127.0.0.1:5000**

## 📱 Usage

### Chat Interface
1. Open your browser and navigate to: `http://127.0.0.1:5000`
2. Type your question in the input box
3. Press Enter or click the send button
4. The chatbot will respond with relevant information
5. Use suggested questions for quick queries

### Admin Dashboard
1. Navigate to: `http://127.0.0.1:5000/admin`
2. View real-time statistics:
   - Total conversations
   - Intent distribution
   - Feedback metrics
   - Confidence scores
3. Browse conversation history
4. Monitor chatbot performance

## 🧠 How NLP Works

### Intent Classification Process

1. **Text Preprocessing**
   - Convert to lowercase
   - Remove special characters
   - Tokenization using NLTK
   - Remove stopwords (keeping important ones)
   - Lemmatization

2. **Intent Matching**
   - Keyword-based scoring
   - Phrase pattern matching
   - Weighted scoring by intent importance
   - Confidence calculation

3. **Entity Extraction**
   - Extract order IDs (e.g., ORD12345)
   - Pattern matching for relevant entities
   - Context-aware extraction

4. **Response Generation**
   - Fetch response template from database
   - Personalize with extracted entities
   - Add suggested follow-up questions

### Example Classification

**User Input:** "Where is my order #12345?"

**Processing:**
- Tokens: ['where', 'order', '12345']
- Intent: `order_status` (confidence: 0.95)
- Entity: `order_id = "12345"`
- Response: Personalized order status message with order ID

## 🗄️ Database Schema

### Conversations Table
```sql
- id: Primary key
- session_id: User session identifier
- user_message: User's query
- bot_response: Chatbot's response
- intent: Detected intent
- confidence: Confidence score (0.0-1.0)
- timestamp: Message timestamp
- ip_address: User's IP
- feedback: User feedback (positive/negative)
```

### FAQ Categories Table
```sql
- id: Primary key
- category: Intent/category name
- response_template: Response text
- keywords: Associated keywords
- is_active: Active status
- created_at: Creation timestamp
- updated_at: Update timestamp
```

## 🔧 Configuration

### Database Configuration

**SQLite (Default):**
```python
# Already configured in config.py
SQLALCHEMY_DATABASE_URI = 'sqlite:///chatbot.db'
```

**MySQL:**
```python
# Update config.py
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/chatbot_db'

# Install MySQL driver
pip install pymysql
```

### Customizing Responses

Edit responses in the database or modify default responses in `app.py`:

```python
# Update FAQ responses
faq = FAQCategory.query.filter_by(category='order_status').first()
faq.response_template = "Your custom response here"
db.session.commit()
```

### Adding New Intents

1. **Add to Intent Classifier** (`nlp/intent_classifier.py`):
```python
self.intents['new_intent'] = {
    'keywords': ['keyword1', 'keyword2'],
    'phrases': ['phrase pattern'],
    'weight': 1.0
}
```

2. **Add Response Template** (via database or code):
```python
new_faq = FAQCategory(
    category='new_intent',
    response_template='Your response here',
    keywords='keyword1,keyword2'
)
db.session.add(new_faq)
db.session.commit()
```

## 📊 API Endpoints

### Chat API
```
POST /api/chat
Body: { "message": "user message" }
Response: { 
    "success": true,
    "response": "bot response",
    "intent": "detected_intent",
    "confidence": 0.95,
    "suggestions": [...],
    "conversation_id": 123
}
```

### Feedback API
```
POST /api/feedback
Body: { 
    "conversation_id": 123, 
    "feedback": "positive" 
}
Response: { 
    "success": true,
    "message": "Thank you for your feedback!"
}
```

### Admin APIs
```
GET /api/admin/conversations?page=1&per_page=50
GET /api/admin/stats
```

## 🎨 Customization

### Changing Colors

Edit CSS variables in `static/css/style.css`:

```css
:root {
    --primary-color: #667eea;       /* Primary color */
    --secondary-color: #764ba2;     /* Secondary color */
    --accent-color: #f093fb;        /* Accent color */
}
```

### Modifying UI Layout

Templates are located in `templates/`:
- `index.html` - Chat interface
- `admin.html` - Admin dashboard

## 🔒 Security Considerations

### For Production Deployment:

1. **Change Secret Key**
```python
# config.py
SECRET_KEY = 'your-secure-random-secret-key'
```

2. **Add Authentication**
- Implement login system for admin panel
- Use Flask-Login or similar

3. **Enable HTTPS**
- Use SSL certificates
- Configure reverse proxy (nginx/Apache)

4. **Input Validation**
- Already implemented (XSS prevention in frontend)
- Add rate limiting for API endpoints

5. **Database Security**
- Use environment variables for credentials
- Enable database encryption

## 🐛 Troubleshooting

### Issue: NLTK Data Not Found
```bash
python -c "import nltk; nltk.download('all')"
```

### Issue: Database Not Created
```bash
# Delete existing database and restart
rm chatbot.db
python app.py
```

### Issue: Port Already in Use
```python
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 📈 Performance Optimization

### For High Traffic:

1. **Use Production Server**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Enable Caching**
```bash
pip install Flask-Caching
```

3. **Database Optimization**
- Add database indexes
- Use connection pooling
- Consider PostgreSQL for better performance

## 🚢 Deployment

### Deploy to Heroku:
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create your-chatbot-name
git push heroku main
```

### Deploy to AWS/GCP:
- Use Elastic Beanstalk or App Engine
- Configure environment variables
- Set up managed database service

## 📝 License

This project is provided as-is for educational and commercial use.

## 🤝 Support

For issues or questions:
- Review the documentation above
- Check admin dashboard for analytics
- Modify NLP patterns in `intent_classifier.py`
- Customize responses in database

## 🎯 Future Enhancements

Potential improvements:
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Integration with ticketing systems
- [ ] Advanced ML models (BERT, GPT)
- [ ] Sentiment analysis
- [ ] Conversation context tracking
- [ ] File upload support
- [ ] Email notifications
- [ ] Live chat handoff to human agents

## 📚 Technologies Used

- **Backend:** Python 3, Flask
- **Database:** SQLite (SQLAlchemy ORM)
- **NLP:** NLTK (Natural Language Toolkit)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **UI Design:** Modern gradient design, responsive layout
- **Icons:** Inline SVG

---

**Developed with ❤️ for excellent customer support experiences**

---

## Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access chat interface
open http://127.0.0.1:5000

# Access admin panel
open http://127.0.0.1:5000/admin
```

Enjoy your intelligent customer support chatbot! 🚀
