from math import radians, sin, cos, sqrt, atan2
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

# Given coordinates
my_location = (22.559146, 88.488639)
user_locations_no = [
    (22.568668, 88.483446, 1, 3),
    (22.552914, 88.473345, 2, 2),
    (22.581797, 88.432317, 2, 2),
    (22.592111, 88.458111, 3, 1),
]

# Check distances and filter users within the radius
radius_km = 5
valid_users = []
for lat, lon, user_id, num_people in user_locations_no:
    distance_km = haversine(my_location[0], my_location[1], lat, lon)
    if distance_km <= radius_km:
        valid_users.append((lat, lon, user_id, num_people, distance_km))

# Efficient pairing based on minimum distance
paired_users = []
used_indices = set()

valid_users.sort(key=lambda x: x[4])  # Sort by distance from my_location

for i in range(len(valid_users)):
    if i in used_indices:
        continue
    best_pair = None
    min_distance = float('inf')
    for j in range(i + 1, len(valid_users)):
        if j in used_indices:
            continue
        dist = haversine(valid_users[i][0], valid_users[i][1], valid_users[j][0], valid_users[j][1])
        if dist < min_distance:
            min_distance = dist
            best_pair = j
    if best_pair is not None:
        paired_users.append((valid_users[i], valid_users[best_pair], min_distance))
        used_indices.add(i)
        used_indices.add(best_pair)

# Print paired users
print("\nEfficiently Paired Users:")
for pair in paired_users:
    print(f"User {pair[0][2]} ({pair[0][0]}, {pair[0][1]}) with {pair[0][3]} people <--> User {pair[1][2]} ({pair[1][0]}, {pair[1][1]}) with {pair[1][3]} people, Distance: {pair[2]:.2f} km")