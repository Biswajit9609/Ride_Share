from math import radians, sin, cos, sqrt, atan2
import pandas as pd

# Haversine formula to calculate distance
def haversine(lat1, lon1, lat2, lon2):
    EARTH_RADIUS_KM = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return EARTH_RADIUS_KM * c

# User Data
user_data = pd.DataFrame({
    'users': ['user1', 'user2', 'user3', 'user4', 'user5', 'user6'],
    'lat': [22.568668, 22.552914, 22.592111, 22.592000, 22.460000, 22.460000],
    'long': [88.483446, 88.473345, 88.432317, 88.458111, 88.220000, 88.220032],
    'flat': [22.580469, 22.572208, 22.562208, 22.552208, 22.542208, 22.532208],
    'flong': [88.415005, 88.412376, 88.402376, 88.392376, 88.382376, 88.372376],
    'no_of_person': [1, 3, 4, 2, 2, 1],
    'booking_status': ['pending'] * 6
})

radius_km = 5  # 5 km radius
assigned_users = set()
groups = []

# Forming ride groups
for i, user in user_data.iterrows():
    if user['users'] in assigned_users:
        continue
    
    possible_group = [(user['users'], user['lat'], user['long'], user['flat'], user['flong'], user['no_of_person'], 0, 0)]
    total_people = user['no_of_person']
    assigned_users.add(user['users'])
    
    for j, other_user in user_data.iterrows():
        if other_user['users'] in assigned_users:
            continue
        
        # Check start location radius
        start_distance = haversine(user['lat'], user['long'], other_user['lat'], other_user['long'])
        # Check final location radius
        end_distance = haversine(user['flat'], user['flong'], other_user['flat'], other_user['flong'])
        
        if start_distance <= radius_km and end_distance <= radius_km and total_people + other_user['no_of_person'] <= 4:
            possible_group.append((other_user['users'], other_user['lat'], other_user['long'], other_user['flat'], other_user['flong'], other_user['no_of_person'], start_distance, end_distance))
            total_people += other_user['no_of_person']
            assigned_users.add(other_user['users'])
        
        if total_people == 4:
            break  # Stop when reaching 4 people
    
    if total_people <= 4:
        groups.append(possible_group)

# Print groups
print("\nFormed Ride Groups:")
for idx, group in enumerate(groups, 1):
    print(f"Group {idx}:")
    for member in group:
        print(f"  {member[0]} - Start: ({member[1]}, {member[2]}) | End: ({member[3]}, {member[4]}) - {member[5]} person(s) | Start Distance: {member[6]:.2f} km | End Distance: {member[7]:.2f} km")
    print()
