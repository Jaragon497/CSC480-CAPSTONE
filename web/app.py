# app.py - Flask Application Factory
import os
from flask import Flask
from web.routes import register_routes


def create_app():
    """Application factory pattern"""
    # Get the parent directory (project root) for templates
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    
    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = "your-secret-key-here"

    # Register all routes
    register_routes(app)

    return app
