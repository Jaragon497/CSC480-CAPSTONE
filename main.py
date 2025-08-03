# main.py - Main Entry Point for Logistics Management Application
from web.app import create_app
from database import init_database, seed_sample_data
from services.background_services import data_aggregator

if __name__ == "__main__":
    # Initialize database
    init_database()
    seed_sample_data()

    # Create Flask app
    app = create_app()

    # Start background services
    data_aggregator.start()

    try:
        app.run(debug=True, threaded=True, host="0.0.0.0", port=5000)
    finally:
        data_aggregator.stop()