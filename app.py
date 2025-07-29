# app.py - Main Flask Application
from flask import Flask
from database import init_database, seed_sample_data
from background_services import data_aggregator
from real_apis import configure_real_apis
from routes import register_routes


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.secret_key = "your-secret-key-here"

    # Register all routes
    register_routes(app)

    return app


if __name__ == "__main__":
    init_database()
    seed_sample_data()

    app = create_app()

    data_aggregator.start()

    try:
        app.run(debug=True, threaded=True, host="0.0.0.0", port=5000)
    finally:
        data_aggregator.stop()
