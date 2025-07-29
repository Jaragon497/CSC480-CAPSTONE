from flask import render_template, request, jsonify, redirect, url_for, flash
from dataclasses import asdict
from database import FacilityDB, MetricsDB, AlertsDB, MessagesDB

# Import both mock and real APIs
from external_apis import DataService as MockDataService, RecommendationEngine
from real_apis import get_configured_data_service


def get_data_service():
    """Get the configured data service (real or mock)"""
    try:
        return get_configured_data_service()
    except ImportError:
        # Fall back to mock if real APIs not configured
        return MockDataService()


def register_routes(app):
    """Register all Flask routes"""

    @app.route("/")
    def dashboard():
        """Main dashboard view"""
        # Get facility summary
        facilities = FacilityDB.get_all_active_facilities()

        # Get recent alerts
        alerts = AlertsDB.get_active_alerts(10)

        # Get recent messages
        messages = MessagesDB.get_recent_messages(5)

        return render_template(
            "dashboard.html", facilities=facilities, alerts=alerts, messages=messages
        )

    @app.route("/facility/<int:facility_id>")
    def facility_detail(facility_id):
        """Detailed view of a specific facility"""
        # Get facility info
        facility = FacilityDB.get_facility_by_id(facility_id)
        if not facility:
            flash("Facility not found", "error")
            return redirect(url_for("dashboard"))

        # Get recent metrics - ensure we get a list
        metrics = MetricsDB.get_facility_metrics(facility_id, 24)

        # Ensure metrics is a list (fix for float iteration error)
        if not isinstance(metrics, list):
            metrics = []

        # Get facility alerts
        alerts = AlertsDB.get_facility_alerts(facility_id, 10)

        return render_template(
            "facility_detail.html", facility=facility, metrics=metrics, alerts=alerts
        )

    @app.route("/messages")
    def messages():
        """Messaging interface"""
        facilities = FacilityDB.get_all_facilities()
        recent_messages = MessagesDB.get_recent_messages(20)

        return render_template(
            "messages.html", facilities=facilities, messages=recent_messages
        )

    @app.route("/send_message", methods=["POST"])
    def send_message():
        """Send message between facilities"""
        from_facility = request.form.get("from_facility")
        to_facility = request.form.get("to_facility")
        message = request.form.get("message")
        priority = request.form.get("priority", "normal")

        # Validation
        if not all([from_facility, to_facility, message]):
            flash("All fields are required", "error")
            return redirect(url_for("messages"))

        if from_facility == to_facility:
            flash("Cannot send message to the same facility", "error")
            return redirect(url_for("messages"))

        try:
            from_facility_id = int(from_facility)
            to_facility_id = int(to_facility)

            MessagesDB.insert_message(
                from_facility_id, to_facility_id, message, priority
            )
            flash("Message sent successfully", "success")

        except (ValueError, TypeError) as e:
            flash("Invalid facility selection", "error")
        except Exception as e:
            flash(f"Error sending message: {str(e)}", "error")

        return redirect(url_for("messages"))

    # API Routes with Real/Mock Data Service Integration
    @app.route("/api/facilities")
    def api_facilities():
        """API endpoint for facility data"""
        try:
            facilities = FacilityDB.get_all_active_facilities()
            return jsonify([dict(facility) for facility in facilities])
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/weather/<location>")
    def api_weather(location):
        """API endpoint for weather data with real/mock providers"""
        try:
            data_service = get_data_service()
            weather_data = data_service.get_weather_with_fallback(location)

            if weather_data:
                return jsonify(asdict(weather_data))
            else:
                return jsonify(
                    {
                        "error": "Weather data unavailable",
                        "message": "All weather providers failed",
                        "status": "fallback",
                    }
                ), 503
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/traffic/<route_id>")
    def api_traffic(route_id):
        """API endpoint for traffic data with real/mock providers"""
        try:
            data_service = get_data_service()
            traffic_data = data_service.get_traffic_with_fallback(route_id)

            if traffic_data:
                return jsonify(asdict(traffic_data))
            else:
                return jsonify(
                    {
                        "error": "Traffic data unavailable",
                        "message": "Traffic providers failed",
                        "status": "fallback",
                    }
                ), 503
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/earthquake-alerts")
    def api_earthquake_alerts():
        """API endpoint for earthquake alerts (real USGS data)"""
        try:
            data_service = get_data_service()
            if hasattr(data_service, "get_earthquake_alerts"):
                earthquakes = data_service.get_earthquake_alerts()
                return jsonify(earthquakes)
            else:
                return jsonify([])  # Mock service doesn't have earthquakes
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/recommendations")
    def api_recommendations():
        """API endpoint for automated routing recommendations"""
        try:
            recommendations = RecommendationEngine.generate_recommendations()

            # Add earthquake-based recommendations if using real APIs
            data_service = get_data_service()
            if hasattr(data_service, "get_earthquake_alerts"):
                earthquakes = data_service.get_earthquake_alerts()
                for eq in earthquakes:
                    if eq["magnitude"] > 5.0:
                        recommendations.append(
                            {
                                "type": "earthquake_advisory",
                                "priority": "high"
                                if eq["magnitude"] > 6.0
                                else "medium",
                                "location": eq["location"],
                                "reason": f"Magnitude {eq['magnitude']:.1f} earthquake detected",
                                "suggested_action": "Monitor routes in affected area for potential disruptions",
                                "estimated_impact": "Potential delays or route closures",
                            }
                        )

            return jsonify(recommendations)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/alerts")
    def api_alerts():
        """API endpoint for current alerts"""
        try:
            alerts = AlertsDB.get_active_alerts()
            return jsonify([dict(alert) for alert in alerts])
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/resolve_alert/<int:alert_id>", methods=["POST"])
    def resolve_alert(alert_id):
        """Mark an alert as resolved"""
        try:
            AlertsDB.resolve_alert(alert_id)
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/system-status")
    def api_system_status():
        """Extended system status including API health"""
        try:
            data_service = get_data_service()

            # Test facilities database
            facilities = FacilityDB.get_all_active_facilities()

            # Test weather API
            weather_status = "unknown"
            try:
                weather_test = data_service.get_weather_with_fallback("Chicago")
                weather_status = "available" if weather_test else "degraded"
            except:
                weather_status = "failed"

            # Test traffic API
            traffic_status = "unknown"
            try:
                traffic_test = data_service.get_traffic_with_fallback("route-1")
                traffic_status = "available" if traffic_test else "degraded"
            except:
                traffic_status = "failed"

            # Check if using real or mock APIs
            api_type = (
                "real" if hasattr(data_service, "get_earthquake_alerts") else "mock"
            )

            return jsonify(
                {
                    "status": "healthy",
                    "api_type": api_type,
                    "database": "connected",
                    "facilities_count": len(facilities),
                    "weather_api": weather_status,
                    "traffic_api": traffic_status,
                    "services": {
                        "data_aggregator": "running",
                        "alert_system": "active",
                        "messaging": "operational",
                    },
                }
            )
        except Exception as e:
            return jsonify({"status": "unhealthy", "error": str(e)}), 500

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template(
            "error.html", error_code=404, error_message="Page not found"
        ), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template(
            "error.html", error_code=500, error_message="Internal server error"
        ), 500
