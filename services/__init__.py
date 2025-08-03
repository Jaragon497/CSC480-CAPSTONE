"""Services module for background services and external APIs"""
from .background_services import data_aggregator, system_monitor, start_all_services, stop_all_services
from .external_apis import DataService, RecommendationEngine
from .real_apis import get_configured_data_service, configure_real_apis

__all__ = [
    'data_aggregator',
    'system_monitor', 
    'start_all_services',
    'stop_all_services',
    'DataService',
    'RecommendationEngine',
    'get_configured_data_service',
    'configure_real_apis'
]