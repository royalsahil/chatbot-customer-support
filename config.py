"""
Configuration file for Flask application
Contains database settings and application configuration
"""
import os

class Config:
    """Base configuration class"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration (Using SQLite for simplicity)
    # You can change this to MySQL by updating the database URI
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'chatbot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application settings
    DEBUG = True
    
    # For MySQL, use this format instead:
    # SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/chatbot_db'
