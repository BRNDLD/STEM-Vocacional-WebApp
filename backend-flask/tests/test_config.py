"""
Test configuration for STEM Vocacional WebApp
"""
import os
import tempfile

class TestConfig:
    """Configuration for testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory SQLite for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ENGINE_OPTIONS = {}
    
    # Override any environment variables
    DB_SERVER = 'test'
    DB_NAME = 'test'
    DB_USER = 'test'
    DB_PASSWORD = 'test'