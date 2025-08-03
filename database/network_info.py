# network_info.py - Network information and utilities

def print_network_summary():
    """Print a summary of the logistics network"""
    from .network_data import get_hubs_only, get_stations_only, get_hub_coverage_map
    
    hubs = get_hubs_only()
    stations = get_stations_only()
    coverage_map = get_hub_coverage_map()
    
    print("=== US LOGISTICS NETWORK SUMMARY ===")
    print(f"Total Facilities: {len(hubs) + len(stations)}")
    print(f"  - Hubs: {len(hubs)}")
    print(f"  - Stations: {len(stations)}")
    print()
    
    print("TIER 1 HUBS (Major National Hubs):")
    tier1_hubs = hubs[:5]  # First 5 are Tier 1
    for hub in tier1_hubs:
        print(f"  • {hub[0]} - {hub[1]} (Capacity: {hub[4]:,})")
    print()
    
    print("TIER 2 HUBS (Regional Hubs):")
    tier2_hubs = hubs[5:12]  # Next 7 are Tier 2
    for hub in tier2_hubs:
        print(f"  • {hub[0]} - {hub[1]} (Capacity: {hub[4]:,})")
    print()
    
    print("TIER 3 HUBS (Secondary Regional Hubs):")
    tier3_hubs = hubs[12:]  # Remaining are Tier 3
    for hub in tier3_hubs:
        print(f"  • {hub[0]} - {hub[1]} (Capacity: {hub[4]:,})")
    print()
    
    print("GEOGRAPHIC COVERAGE:")
    regions = {
        'Northeast': ['New York Metro Hub', 'Philadelphia Northeast Hub'],
        'Southeast': ['Atlanta Southeast Hub', 'Miami Southeast Hub', 'Charlotte Southeast Hub', 'Raleigh Research Triangle Hub'],
        'Midwest': ['Chicago Central Hub', 'Indianapolis Midwest Hub', 'Kansas City Central Hub', 'Cincinnati Ohio Valley Hub'],
        'South': ['Dallas-Fort Worth Hub', 'Houston Gulf Hub', 'Memphis Mid-South Hub', 'Nashville Tennessee Hub'],
        'West': ['Los Angeles Hub', 'Phoenix Southwest Hub', 'Seattle Northwest Hub', 'Portland Northwest Hub', 'Salt Lake City Mountain Hub', 'Denver Mountain Hub']
    }
    
    for region, region_hubs in regions.items():
        hub_count = len([h for h in hubs if h[0] in region_hubs])
        station_count = len([s for s in stations if any(coverage_map.get(hub_name, []) and s[0] in coverage_map[hub_name] for hub_name in region_hubs if hub_name in [h[0] for h in hubs])])
        print(f"  {region}: {hub_count} hubs, {station_count}+ stations")
    
    print()
    print("KEY LOGISTICS CORRIDORS:")
    print("  • I-80 Corridor: Chicago ↔ Denver ↔ Salt Lake City ↔ Los Angeles")
    print("  • I-75 Corridor: Miami ↔ Atlanta ↔ Cincinnati ↔ Chicago")
    print("  • I-10 Corridor: Los Angeles ↔ Phoenix ↔ Houston ↔ Miami")
    print("  • I-95 Corridor: Miami ↔ Charlotte ↔ Raleigh ↔ New York ↔ Philadelphia")
    print("  • I-35 Corridor: Dallas ↔ Kansas City ↔ Minneapolis")

def get_network_stats():
    """Get network statistics"""
    from .network_data import get_all_facilities, get_all_routes, get_hubs_only, get_stations_only
    
    facilities = get_all_facilities()
    routes = get_all_routes()
    hubs = get_hubs_only()
    stations = get_stations_only()
    
    total_hub_capacity = sum(hub[4] for hub in hubs)
    total_station_capacity = sum(station[4] for station in stations)
    
    stats = {
        'total_facilities': len(facilities),
        'total_hubs': len(hubs),
        'total_stations': len(stations),
        'total_routes': len(routes),
        'total_hub_capacity': total_hub_capacity,
        'total_station_capacity': total_station_capacity,
        'total_network_capacity': total_hub_capacity + total_station_capacity,
        'avg_hub_capacity': total_hub_capacity // len(hubs),
        'avg_station_capacity': total_station_capacity // len(stations),
        'largest_hub': max(hubs, key=lambda x: x[4]),
        'largest_station': max(stations, key=lambda x: x[4])
    }
    
    return stats

if __name__ == "__main__":
    print_network_summary()
    print()
    stats = get_network_stats()
    print("=== NETWORK STATISTICS ===")
    for key, value in stats.items():
        if key in ['largest_hub', 'largest_station']:
            print(f"{key.replace('_', ' ').title()}: {value[0]} ({value[4]:,} capacity)")
        else:
            print(f"{key.replace('_', ' ').title()}: {value:,}" if isinstance(value, int) else f"{key.replace('_', ' ').title()}: {value}")