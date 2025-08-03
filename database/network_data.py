# network_data.py - Comprehensive logistics network data for the US

# Strategic Hub Locations (20 major hubs in key metropolitan areas)
# These are positioned for maximum coverage and efficiency across the US logistics network
# Format: (name, location, type, status, max_capacity, current_load, staff_count)
LOGISTICS_HUBS = [
    # Tier 1 - Major National Hubs (300 staff)
    ("Chicago Central Hub", "Chicago, IL", "hub", "active", 5000, 3200, 300),
    ("Los Angeles Hub", "Los Angeles, CA", "hub", "active", 4500, 2800, 290),
    ("Atlanta Southeast Hub", "Atlanta, GA", "hub", "active", 4200, 2600, 285),
    ("Dallas-Fort Worth Hub", "Dallas, TX", "hub", "active", 4000, 2400, 280),
    ("New York Metro Hub", "Newark, NJ", "hub", "active", 3800, 2300, 275),
    
    # Tier 2 - Regional Hubs (200-250 staff)
    ("Denver Mountain Hub", "Denver, CO", "hub", "active", 3500, 2100, 250),
    ("Memphis Mid-South Hub", "Memphis, TN", "hub", "active", 3200, 1900, 245),
    ("Phoenix Southwest Hub", "Phoenix, AZ", "hub", "active", 3000, 1800, 240),
    ("Seattle Northwest Hub", "Seattle, WA", "hub", "active", 2800, 1700, 235),
    ("Miami Southeast Hub", "Miami, FL", "hub", "active", 2700, 1600, 230),
    ("Indianapolis Midwest Hub", "Indianapolis, IN", "hub", "active", 2600, 1550, 225),
    ("Kansas City Central Hub", "Kansas City, MO", "hub", "active", 2500, 1500, 220),
    
    # Tier 3 - Secondary Regional Hubs (100-200 staff)
    ("Charlotte Southeast Hub", "Charlotte, NC", "hub", "active", 2400, 1450, 200),
    ("Cincinnati Ohio Valley Hub", "Cincinnati, OH", "hub", "active", 2300, 1400, 190),
    ("Portland Northwest Hub", "Portland, OR", "hub", "active", 2200, 1350, 180),
    ("Houston Gulf Hub", "Houston, TX", "hub", "active", 2100, 1300, 175),
    ("Philadelphia Northeast Hub", "Philadelphia, PA", "hub", "active", 2000, 1250, 170),
    ("Salt Lake City Mountain Hub", "Salt Lake City, UT", "hub", "active", 1900, 1200, 160),
    ("Nashville Tennessee Hub", "Nashville, TN", "hub", "active", 1800, 1150, 150),
    ("Raleigh Research Triangle Hub", "Raleigh, NC", "hub", "active", 1700, 1100, 140),
]

# Strategic Station Locations (51 stations positioned around hubs)
# Stations handle last-mile delivery and local distribution
# Format: (name, location, type, status, max_capacity, current_load, staff_count)
LOGISTICS_STATIONS = [
    # Chicago Hub Coverage Area
    ("Milwaukee Station", "Milwaukee, WI", "station", "active", 1200, 700, 28),
    ("Madison Station", "Madison, WI", "station", "active", 800, 450, 22),
    ("Rockford Station", "Rockford, IL", "station", "active", 600, 350, 18),
    ("Peoria Station", "Peoria, IL", "station", "active", 700, 400, 20),
    
    # Los Angeles Hub Coverage Area
    ("San Diego Station", "San Diego, CA", "station", "active", 1500, 900, 30),
    ("Riverside Station", "Riverside, CA", "station", "active", 1000, 600, 25),
    ("Bakersfield Station", "Bakersfield, CA", "station", "active", 800, 480, 22),
    ("Fresno Station", "Fresno, CA", "station", "active", 900, 540, 24),
    ("Ventura Station", "Ventura, CA", "station", "active", 700, 420, 19),
    
    # Atlanta Hub Coverage Area
    ("Birmingham Station", "Birmingham, AL", "station", "active", 1100, 660, 26),
    ("Columbia Station", "Columbia, SC", "station", "active", 900, 540, 23),
    ("Savannah Station", "Savannah, GA", "station", "active", 800, 480, 21),
    ("Augusta Station", "Augusta, GA", "station", "active", 600, 360, 17),
    
    # Dallas-Fort Worth Hub Coverage Area
    ("San Antonio Station", "San Antonio, TX", "station", "active", 1300, 780, 29),
    ("Austin Station", "Austin, TX", "station", "active", 1100, 660, 26),
    ("Waco Station", "Waco, TX", "station", "active", 500, 300, 15),
    ("Tyler Station", "Tyler, TX", "station", "active", 600, 360, 17),
    
    # New York Metro Hub Coverage Area
    ("Albany Station", "Albany, NY", "station", "active", 800, 480, 21),
    ("Trenton Station", "Trenton, NJ", "station", "active", 700, 420, 19),
    ("Hartford Station", "Hartford, CT", "station", "active", 900, 540, 23),
    ("Allentown Station", "Allentown, PA", "station", "active", 750, 450, 20),
    
    # Denver Hub Coverage Area
    ("Colorado Springs Station", "Colorado Springs, CO", "station", "active", 900, 540, 23),
    ("Boulder Station", "Boulder, CO", "station", "active", 600, 360, 17),
    ("Fort Collins Station", "Fort Collins, CO", "station", "active", 700, 420, 19),
    ("Grand Junction Station", "Grand Junction, CO", "station", "active", 500, 300, 15),
    
    # Memphis Hub Coverage Area
    ("Little Rock Station", "Little Rock, AR", "station", "active", 800, 480, 21),
    ("Jackson Station", "Jackson, MS", "station", "active", 700, 420, 19),
    ("Tupelo Station", "Tupelo, MS", "station", "active", 400, 240, 12),
    
    # Phoenix Hub Coverage Area
    ("Tucson Station", "Tucson, AZ", "station", "active", 1000, 600, 25),
    ("Flagstaff Station", "Flagstaff, AZ", "station", "active", 500, 300, 15),
    ("Yuma Station", "Yuma, AZ", "station", "active", 600, 360, 17),
    
    # Seattle Hub Coverage Area
    ("Spokane Station", "Spokane, WA", "station", "active", 800, 480, 21),
    ("Tacoma Station", "Tacoma, WA", "station", "active", 900, 540, 23),
    ("Bellingham Station", "Bellingham, WA", "station", "active", 500, 300, 15),
    ("Yakima Station", "Yakima, WA", "station", "active", 600, 360, 17),
    
    # Miami Hub Coverage Area
    ("Tampa Station", "Tampa, FL", "station", "active", 1200, 720, 28),
    ("Orlando Station", "Orlando, FL", "station", "active", 1100, 660, 26),
    ("Jacksonville Station", "Jacksonville, FL", "station", "active", 1000, 600, 25),
    ("Fort Lauderdale Station", "Fort Lauderdale, FL", "station", "active", 800, 480, 21),
    
    # Indianapolis Hub Coverage Area
    ("Fort Wayne Station", "Fort Wayne, IN", "station", "active", 700, 420, 19),
    ("Evansville Station", "Evansville, IN", "station", "active", 600, 360, 17),
    ("South Bend Station", "South Bend, IN", "station", "active", 650, 390, 18),
    
    # Kansas City Hub Coverage Area
    ("Topeka Station", "Topeka, KS", "station", "active", 500, 300, 15),
    ("Springfield Station", "Springfield, MO", "station", "active", 700, 420, 19),
    ("Omaha Station", "Omaha, NE", "station", "active", 900, 540, 23),
    
    # Charlotte Hub Coverage Area
    ("Greensboro Station", "Greensboro, NC", "station", "active", 800, 480, 21),
    ("Asheville Station", "Asheville, NC", "station", "active", 600, 360, 17),
    ("Greenville Station", "Greenville, SC", "station", "active", 700, 420, 19),
    
    # Additional Strategic Stations
    ("Boise Station", "Boise, ID", "station", "active", 800, 480, 21),
    ("Albuquerque Station", "Albuquerque, NM", "station", "active", 900, 540, 23),
    ("Richmond Station", "Richmond, VA", "station", "active", 1000, 600, 25),
]

# Strategic Route Connections (Hub-to-Hub and Hub-to-Station)
# Based on major interstate highways and optimal logistics flow
LOGISTICS_ROUTES = [
    # Primary Hub-to-Hub Connections (Tier 1 routes)
    # Major cross-country corridors
    (1, 2, 2015, 29.5),   # Chicago to Los Angeles (I-80/I-76)
    (1, 3, 720, 11.2),    # Chicago to Atlanta (I-65)
    (1, 4, 925, 14.5),    # Chicago to Dallas (I-55/I-35)
    (1, 5, 790, 12.8),    # Chicago to New York (I-80)
    (2, 8, 370, 5.8),     # Los Angeles to Phoenix (I-10)
    (3, 10, 665, 10.2),   # Atlanta to Miami (I-75)
    (4, 16, 925, 14.2),   # Dallas to Houston (I-45)
    
    # Secondary Hub-to-Hub Connections (Tier 2 routes)
    (1, 6, 920, 14.5),    # Chicago to Denver (I-80)
    (1, 11, 350, 5.5),    # Chicago to Indianapolis (I-65)
    (3, 13, 245, 4.0),    # Atlanta to Charlotte (I-85)
    (4, 8, 430, 6.8),     # Dallas to Phoenix (I-20/I-10)
    (5, 17, 95, 1.8),     # New York to Philadelphia (I-95)
    (6, 18, 500, 7.8),    # Denver to Salt Lake City (I-80)
    (7, 4, 300, 4.8),     # Memphis to Dallas (I-40)
    (9, 15, 175, 2.8),    # Seattle to Portland (I-5)
    
    # Regional Hub Connections
    (11, 12, 300, 4.8),   # Indianapolis to Kansas City (I-70)
    (13, 20, 130, 2.2),   # Charlotte to Raleigh (I-85)
    (14, 11, 110, 1.8),   # Cincinnati to Indianapolis (I-74)
    (19, 7, 180, 2.8),    # Nashville to Memphis (I-40)
    
    # Chicago Hub to Station Connections
    (1, 21, 90, 1.5),     # Chicago to Milwaukee
    (1, 22, 150, 2.5),    # Chicago to Madison
    (1, 23, 90, 1.5),     # Chicago to Rockford
    (1, 24, 165, 2.8),    # Chicago to Peoria
    
    # Los Angeles Hub to Station Connections
    (2, 25, 120, 2.0),    # Los Angeles to San Diego
    (2, 26, 60, 1.0),     # Los Angeles to Riverside
    (2, 27, 110, 1.8),    # Los Angeles to Bakersfield
    (2, 28, 220, 3.5),    # Los Angeles to Fresno
    (2, 29, 65, 1.2),     # Los Angeles to Ventura
    
    # Atlanta Hub to Station Connections
    (3, 30, 150, 2.5),    # Atlanta to Birmingham
    (3, 31, 215, 3.5),    # Atlanta to Columbia
    (3, 32, 250, 4.0),    # Atlanta to Savannah
    (3, 33, 150, 2.5),    # Atlanta to Augusta
    
    # Dallas Hub to Station Connections
    (4, 34, 275, 4.5),    # Dallas to San Antonio
    (4, 35, 195, 3.2),    # Dallas to Austin
    (4, 36, 95, 1.5),     # Dallas to Waco
    (4, 37, 100, 1.8),    # Dallas to Tyler
    
    # New York Hub to Station Connections
    (5, 38, 150, 2.8),    # New York to Albany
    (5, 39, 65, 1.2),     # New York to Trenton
    (5, 40, 110, 2.0),    # New York to Hartford
    (5, 41, 90, 1.8),     # New York to Allentown
    
    # Denver Hub to Station Connections
    (6, 42, 75, 1.2),     # Denver to Colorado Springs
    (6, 43, 30, 0.5),     # Denver to Boulder
    (6, 44, 65, 1.0),     # Denver to Fort Collins
    (6, 45, 245, 4.0),    # Denver to Grand Junction
    
    # Memphis Hub to Station Connections
    (7, 46, 135, 2.2),    # Memphis to Little Rock
    (7, 47, 210, 3.5),    # Memphis to Jackson
    (7, 48, 105, 1.8),    # Memphis to Tupelo
    
    # Phoenix Hub to Station Connections
    (8, 49, 115, 1.8),    # Phoenix to Tucson
    (8, 50, 145, 2.5),    # Phoenix to Flagstaff
    (8, 51, 180, 3.0),    # Phoenix to Yuma
    
    # Seattle Hub to Station Connections
    (9, 52, 280, 4.5),    # Seattle to Spokane
    (9, 53, 35, 0.6),     # Seattle to Tacoma
    (9, 54, 90, 1.5),     # Seattle to Bellingham
    (9, 55, 140, 2.5),    # Seattle to Yakima
    
    # Miami Hub to Station Connections
    (10, 56, 280, 4.5),   # Miami to Tampa
    (10, 57, 235, 3.8),   # Miami to Orlando
    (10, 58, 345, 5.5),   # Miami to Jacksonville
    (10, 59, 30, 0.5),    # Miami to Fort Lauderdale
    
    # Indianapolis Hub to Station Connections
    (11, 60, 120, 2.0),   # Indianapolis to Fort Wayne
    (11, 61, 170, 2.8),   # Indianapolis to Evansville
    (11, 62, 145, 2.5),   # Indianapolis to South Bend
    
    # Kansas City Hub to Station Connections
    (12, 63, 65, 1.0),    # Kansas City to Topeka
    (12, 64, 165, 2.8),   # Kansas City to Springfield
    (12, 65, 200, 3.2),   # Kansas City to Omaha
    
    # Charlotte Hub to Station Connections
    (13, 66, 90, 1.5),    # Charlotte to Greensboro
    (13, 67, 130, 2.2),   # Charlotte to Asheville
    (13, 68, 100, 1.8),   # Charlotte to Greenville
    
    # Additional Strategic Station Connections
    (18, 69, 300, 4.8),   # Salt Lake City to Boise
    (8, 70, 450, 7.2),    # Phoenix to Albuquerque
    (20, 71, 160, 2.8),   # Raleigh to Richmond
]

def get_all_facilities():
    """Get all facilities (hubs and stations)"""
    return LOGISTICS_HUBS + LOGISTICS_STATIONS

def get_all_routes():
    """Get all routes"""
    return LOGISTICS_ROUTES

def get_hubs_only():
    """Get only hub facilities"""
    return LOGISTICS_HUBS

def get_stations_only():
    """Get only station facilities"""
    return LOGISTICS_STATIONS

def get_hub_coverage_map():
    """Get a mapping of hubs to their coverage stations"""
    hub_coverage = {
        "Chicago Central Hub": ["Milwaukee Station", "Madison Station", "Rockford Station", "Peoria Station"],
        "Los Angeles Hub": ["San Diego Station", "Riverside Station", "Bakersfield Station", "Fresno Station", "Ventura Station"],
        "Atlanta Southeast Hub": ["Birmingham Station", "Columbia Station", "Savannah Station", "Augusta Station"],
        "Dallas-Fort Worth Hub": ["San Antonio Station", "Austin Station", "Waco Station", "Tyler Station"],
        "New York Metro Hub": ["Albany Station", "Trenton Station", "Hartford Station", "Allentown Station"],
        "Denver Mountain Hub": ["Colorado Springs Station", "Boulder Station", "Fort Collins Station", "Grand Junction Station"],
        "Memphis Mid-South Hub": ["Little Rock Station", "Jackson Station", "Tupelo Station"],
        "Phoenix Southwest Hub": ["Tucson Station", "Flagstaff Station", "Yuma Station"],
        "Seattle Northwest Hub": ["Spokane Station", "Tacoma Station", "Bellingham Station", "Yakima Station"],
        "Miami Southeast Hub": ["Tampa Station", "Orlando Station", "Jacksonville Station", "Fort Lauderdale Station"],
        "Indianapolis Midwest Hub": ["Fort Wayne Station", "Evansville Station", "South Bend Station"],
        "Kansas City Central Hub": ["Topeka Station", "Springfield Station", "Omaha Station"],
        "Charlotte Southeast Hub": ["Greensboro Station", "Asheville Station", "Greenville Station"],
    }
    return hub_coverage