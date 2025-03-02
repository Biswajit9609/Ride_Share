from math import radians, sin, cos, sqrt, atan2
import pandas as pd
from itertools import combinations

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points on Earth using the Haversine formula."""
    EARTH_RADIUS_KM = 6371  # Radius of Earth in kilometers
    
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Compute deltas
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Apply the Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return EARTH_RADIUS_KM * c  # Distance in kilometers

# User Data
user_data = pd.DataFrame({
    'users': ['user1', 'user2', 'user3', 'user4', 'user5', 'user6'],
    'lat': [22.568668, 22.552914, 22.592111, 22.592000, 22.460000, 22.460000],
    'long': [88.483446, 88.473345, 88.432317, 88.458111, 88.220000, 88.220032],
    'no_of_person': [1, 3, 4, 2, 2, 1],
    'booking_status': ['pending'] * 6
})

radius_km = 5
assigned_users = set()
groups = []

# Create groups ensuring a total of 4 people per group
for i, user in user_data.iterrows():
    if user['users'] in assigned_users:
        continue
    
    possible_group = [(user['users'], user['lat'], user['long'], user['no_of_person'])]
    total_people = user['no_of_person']
    assigned_users.add(user['users'])
    
    for j, other_user in user_data.iterrows():
        if other_user['users'] in assigned_users:
            continue
        
        distance = haversine(user['lat'], user['long'], other_user['lat'], other_user['long'])
        if distance <= radius_km and total_people + other_user['no_of_person'] <= 4:
            possible_group.append((other_user['users'], other_user['lat'], other_user['long'], other_user['no_of_person']))
            total_people += other_user['no_of_person']
            assigned_users.add(other_user['users'])
        
        if total_people <= 4:
            break  # Stop when we reach 4 people
    
    if total_people <= 4:
        groups.append(possible_group)

# Print groups
print("\nFormed Ride Groups:")
for idx, group in enumerate(groups, 1):
    print(f"Group {idx}:")
    for member in group:
        print(f"  {member[0]} - ({member[1]}, {member[2]}) - {member[3]} person(s)")
    print()
