# replit.md

## Overview

This is a **Customer Support Chatbot** — a web-based intelligent chatbot built with Python Flask that uses Natural Language Processing (NLTK) for intent recognition and automatic response generation. Users interact through a real-time chat interface, and admins can view conversation analytics through a dashboard. The chatbot understands natural language queries about order status, cancellations, refunds, product info, and contact support, then responds with appropriate templated answers.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend: Python Flask
- **Framework:** Flask 3.0.0 serves as the web framework, handling both page rendering (Jinja2 templates) and a RESTful JSON API.
- **Entry point:** `app.py` — initializes the Flask app, database, NLP components, and defines routes.
- **Configuration:** `config.py` — uses a `Config` class with environment variable overrides. Database URI defaults to SQLite (`chatbot.db` in the project root) but supports PostgreSQL via the `DATABASE_URL` environment variable. `psycopg2-binary` is included in dependencies for Postgres support.
- **CORS:** Enabled via Flask-CORS for API requests.
- **Session management:** Flask sessions with a secret key for tracking conversations.

### NLP Module (`nlp/`)
- **Intent Classifier** (`nlp/intent_classifier.py`): Uses NLTK for text preprocessing — tokenization, lemmatization, stopword removal. Classifies user messages into intents (greeting, order_status, order_cancellation, refund_policy, contact_support, product_info, thanks, farewell) using keyword/phrase pattern matching with weighted confidence scoring (0.0–1.0). Also extracts entities like order IDs (e.g., ORD12345).
- **Response Generator** (`nlp/responses.py`): Retrieves response templates from the database (`FAQCategory` table). Falls back to hardcoded responses if database templates aren't available. Personalizes responses with extracted entities. Uses a confidence threshold of 0.3 — below that, returns a fallback "I didn't understand" response.
- NLTK data packages (`punkt`, `stopwords`, `wordnet`) are auto-downloaded at import time if missing.

### Database: Flask-SQLAlchemy with SQLite/PostgreSQL
- **ORM:** Flask-SQLAlchemy 3.1.1
- **Default DB:** SQLite file (`chatbot.db`) for local development
- **Production DB:** PostgreSQL supported via `DATABASE_URL` environment variable
- **Models** (`database/models.py`):
  - `Conversation` — stores each chat exchange with fields: `id`, `session_id`, `user_message`, `bot_response`, `intent`, `confidence`, `timestamp`, `ip_address`, `feedback`. Indexed on `session_id`.
  - `FAQCategory` — stores response templates per intent category, with an `is_active` flag for enabling/disabling responses.
- **Initialization:** Tables are auto-created on first run via `db.create_all()`. Default FAQ categories are seeded if the table is empty.

### Frontend
- **Templates:** Server-rendered Jinja2 templates in `templates/`
  - `index.html` — main chat interface
  - `admin.html` — admin analytics dashboard
- **Styling:** `static/css/style.css` — premium design with CSS variables, gradients, glass-morphism effects, animations. Uses Inter font from Google Fonts. Fully responsive.
- **JavaScript:** `static/js/chat.js` — handles chat UI, sends messages to `/api/chat` via fetch API, manages typing indicators, suggested questions, and persists conversation history in localStorage.

### API Endpoints
- `GET /` — serves the chat interface
- `GET /admin` — serves the admin dashboard
- `POST /api/chat` — accepts user message, returns bot response with intent and confidence
- `POST /api/feedback` — submit feedback on a bot response
- `GET /api/admin/conversations` — paginated conversation history
- `GET /api/admin/stats` — chatbot analytics (intent distribution, confidence, feedback)

### Key Design Decisions
1. **NLTK over ML models:** Chose keyword/pattern matching with NLTK preprocessing over training a machine learning classifier. This keeps the system simple, requires no training data, and works out of the box. Tradeoff: less flexible for novel phrasings.
2. **SQLite default with Postgres support:** SQLite for easy local development, Postgres for production. The `DATABASE_URL` env var controls which is used.
3. **Server-side rendering + API:** Templates for pages, but chat communication happens via JSON API calls. This hybrid approach keeps things simple while enabling responsive chat UX.
4. **No authentication:** The admin dashboard has no auth protection — this should be added for production use.

## External Dependencies

### Python Packages (requirements.txt)
- `Flask==3.0.0` — web framework
- `Flask-SQLAlchemy==3.1.1` — ORM for database
- `Flask-CORS==4.0.0` — cross-origin request support
- `nltk==3.8.1` — natural language processing
- `python-dotenv==1.0.0` — environment variable loading
- `gunicorn` — production WSGI server
- `psycopg2-binary` — PostgreSQL driver

### External Services
- **Google Fonts CDN** — Inter font family loaded in templates
- **No other external APIs** — all NLP processing is local

### Database
- **SQLite** (default) — file-based, no setup needed
- **PostgreSQL** (optional) — set `DATABASE_URL` environment variable to connect

### NLTK Data
- `punkt` — tokenizer models
- `stopwords` — English stopword list
- `wordnet` — lemmatizer dictionary
- Auto-downloaded on first run if not present