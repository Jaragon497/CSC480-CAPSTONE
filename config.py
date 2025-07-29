import os
from real_apis import configure_real_apis


# Configuration settings
class Config:
    """Base configuration"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key-here"

    # Real API Configuration
    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
    TOMTOM_API_KEY = os.environ.get("TOMTOM_API_KEY")

    # Enable real APIs (set to False to use mock APIs)
    USE_REAL_APIS = True

    @classmethod
    def init_apis(cls):
        """Initialize API configuration"""
        configure_real_apis(
            openweather_key=cls.OPENWEATHER_API_KEY,
            tomtom_key=cls.TOMTOM_API_KEY,
            enable=cls.USE_REAL_APIS,
        )


# Development configuration with real APIs
class DevelopmentConfig(Config):
    """Development configuration with real APIs enabled"""

    DEBUG = True
    USE_REAL_APIS = True

    # Add your API keys here for development
    OPENWEATHER_API_KEY = "your_openweather_api_key_here"
    TOMTOM_API_KEY = "your_tomtom_api_key_here"


# Production configuration
class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    USE_REAL_APIS = True


# Testing configuration (always use mock APIs)
class TestingConfig(Config):
    """Testing configuration with mock APIs"""

    TESTING = True
    USE_REAL_APIS = False


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": Config,
}


def get_config(config_name=None):
    """Get configuration based on environment"""
    config_name = config_name or os.environ.get("FLASK_ENV", "default")
    return config.get(config_name, Config)


# Example usage in app.py:
"""
from config import get_config

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Initialize APIs
    config_class.init_apis()
    
    # Register routes
    register_routes(app)
    
    return app
"""
