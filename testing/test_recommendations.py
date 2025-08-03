#!/usr/bin/env python3
# Test script for recommendation engine
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import init_database, seed_sample_data
from services.external_apis import RecommendationEngine

def test_recommendations():
    """Test the recommendation engine for temp agency suggestions"""
    print("Testing Recommendation Engine...")
    print("=" * 50)
    
    recommendations = RecommendationEngine.generate_recommendations()
    
    print(f"Generated {len(recommendations)} recommendations:")
    print()
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. Type: {rec['type']}")
        print(f"   Priority: {rec['priority']}")
        print(f"   Facility: {rec.get('source_facility', rec.get('location', 'N/A'))}")
        print(f"   Reason: {rec['reason']}")
        print(f"   Action: {rec.get('suggested_action', 'N/A')}")
        print(f"   Impact: {rec['estimated_impact']}")
        print()
    
    # Count staffing recommendations
    staffing_recs = [r for r in recommendations if r['type'] == 'staffing_shortage']
    print(f"Temp Agency Recommendations: {len(staffing_recs)} found")
    
    return len(staffing_recs) > 0

if __name__ == "__main__":
    # Initialize database if needed
    if not os.path.exists('logistics.db'):
        init_database()
        seed_sample_data()
    
    success = test_recommendations()
    if success:
        print("✅ Temp agency recommendations are working!")
    else:
        print("⚠️  No temp agency recommendations generated")