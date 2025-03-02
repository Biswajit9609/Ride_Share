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


user_data = pd.read_csv('user_data.csv')

radius_km = 5  # 5 km radius

def find_group_for_user(selected_user):
    user_row = user_data[user_data['first_name'] == selected_user]
    
    if user_row.empty:
        print(f"User '{selected_user}' not found.")
        return []

    user_row = user_row.iloc[0]
    user_lat, user_long = user_row['lat'], user_row['long']
    user_flat, user_flong = user_row['flat'], user_row['flong']
    total_people = user_row['no_of_person']

    possible_group = [(selected_user, user_lat, user_long, user_flat, user_flong, user_row['no_of_person'], 0, 0)]
    
    for _, other_user in user_data.iterrows():
        if other_user['first_name'] == selected_user:
            continue
        
        # Calculate start and end distances
        start_distance = haversine(user_lat, user_long, other_user['lat'], other_user['long'])
        end_distance = haversine(user_flat, user_flong, other_user['flat'], other_user['flong'])

        # Check if the user can be added
        if start_distance <= radius_km and end_distance <= radius_km and total_people + other_user['no_of_person'] <= 4:
            possible_group.append((
                other_user['first_name'], other_user['lat'], other_user['long'], 
                other_user['flat'], other_user['flong'], 
                other_user['no_of_person'], start_distance, end_distance
            ))
            total_people += other_user['no_of_person']

        if total_people == 4:  # Stop when reaching max capacity
            break

    # Print group info
    print(f"\nPossible Group for {selected_user}:")
    for member in possible_group:
        print(f"  {member[0]} - Start: ({member[1]}, {member[2]}) | End: ({member[3]}, {member[4]}) - {member[5]} person(s) | Start Distance: {member[6]:.2f} km | End Distance: {member[7]:.2f} km")
    print()
    
    return possible_group

# Example: Find group for 'user1'
selected_user = "user4"
group = find_group_for_user(selected_user)
print(group)
