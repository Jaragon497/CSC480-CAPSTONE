#!/usr/bin/env python3
# test_network.py - Test the new network data
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_database, seed_sample_data, FacilityDB

if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    
    print("Seeding network data...")
    seed_sample_data()
    
    print("Verifying data...")
    facilities = FacilityDB.get_all_active_facilities()
    hubs = [f for f in facilities if f['facility_type'] == 'hub']
    stations = [f for f in facilities if f['facility_type'] == 'station']
    
    print(f"Successfully loaded {len(facilities)} total facilities:")
    print(f"  - {len(hubs)} hubs")
    print(f"  - {len(stations)} stations")
    
    print("\nSample hubs:")
    for hub in hubs[:5]:
        print(f"  - {hub['name']} ({hub['location']}) - Capacity: {hub['max_capacity']}")
    
    print("\nSample stations:")
    for station in stations[:5]:
        print(f"  - {station['name']} ({station['location']}) - Capacity: {station['max_capacity']}")