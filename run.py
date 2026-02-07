"""
Run script for Customer Support Chatbot
"""
from app import app, init_database

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Run the application on port 8080
    print("=" * 50)
    print("🤖 Customer Support Chatbot Starting...")
    print("=" * 50)
    print("📍 Server running at: http://localhost:8080")
    print("💬 Chat Interface: http://localhost:8080")
    print("⚙️  Admin Panel: http://localhost:8080/admin")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8080)
