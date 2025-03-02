from math import radians, sin, cos, sqrt, atan2
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify , send_from_directory, redirect ,make_response
from flask_mail import Mail, Message 
from werkzeug.security import generate_password_hash, check_password_hash
import random
from dotenv import load_dotenv
from config import Config  

app = Flask(__name__)
load_dotenv()

app.config.from_object(Config)
mail = Mail(app)

user_data = pd.read_csv("user_data.csv")

# Haversine formula to calculate distance
def haversine(lat1, lon1, lat2, lon2):
    EARTH_RADIUS_KM = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return EARTH_RADIUS_KM * c

radius_km = 5

def find_group_for_user(selected_user):
    user_row = user_data[user_data['users'] == selected_user]
    
    if user_row.empty:
        print(f"User '{selected_user}' not found.")
        return []

    user_row = user_row.iloc[0]
    user_lat, user_long = user_row['lat'], user_row['long']
    user_flat, user_flong = user_row['flat'], user_row['flong']
    total_people = user_row['no_of_person']

    possible_group = [(selected_user, user_lat, user_long, user_flat, user_flong, user_row['no_of_person'], 0, 0)]
    
    for _, other_user in user_data.iterrows():
        if other_user['users'] == selected_user:
            continue
        
        # Calculate start and end distances
        start_distance = haversine(user_lat, user_long, other_user['lat'], other_user['long'])
        end_distance = haversine(user_flat, user_flong, other_user['flat'], other_user['flong'])

        # Check if the user can be added
        if start_distance <= radius_km and end_distance <= radius_km and total_people + other_user['no_of_person'] <= 4:
            possible_group.append((
                other_user['users'], other_user['lat'], other_user['long'], 
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

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global user_data  # Ensure we are modifying the global DataFrame
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            return "Passwords do not match!", 400

        if email in user_data['email'].values:
            return "Email already exists!", 400

        session['temp_user'] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'password': generate_password_hash(password)
        }

        return redirect(url_for('send_otp'))
    
    return render_template('Sign_up.html')

@app.route('/send_otp', methods=['GET', 'POST'])
def send_otp():
    user_data = session.get('temp_user')
    if not user_data:
        return redirect(url_for('signup'))
    
    email = user_data['email']
    otp = random.randint(100000, 999999)
    session['otp'] = otp

    msg = Message('Your OTP', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Your OTP is {otp}'
    mail.send(msg)

    return redirect(url_for('verify_otp'))

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    global user_data  # Ensure we modify the DataFrame
    
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if 'otp' in session and entered_otp == str(session['otp']):
            session.pop('otp', None)
            user_data_new = session.pop('temp_user', None)
            
            if user_data_new:
                # Convert to DataFrame before appending
                new_entry = pd.DataFrame([user_data_new])
                user_data = pd.concat([user_data, new_entry], ignore_index=True)
                
                # Save to CSV
                user_data.to_csv("user_data.csv", index=False)

                session['user'] = user_data_new['first_name']
                session['email'] = user_data_new['email']
                return redirect(url_for('home'))
            else:
                return "Invalid user data.", 400
        else:
            return "Invalid OTP. Please try again.", 400
    return render_template('otp_verification.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_data  # Reload updated user data
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Reload CSV to get updated data
        user_data = pd.read_csv("user_data.csv")

        user_row = user_data[user_data['email'] == email]
        
        if not user_row.empty:
            stored_password = user_row.iloc[0]['password']
            if check_password_hash(stored_password, password):
                session['user'] = user_row.iloc[0]['first_name']
                session['email'] = email
                return redirect(url_for('home'))
            else:
                return 'Incorrect password, try again.', 400
        else:
            return 'Email does not exist.', 400
    
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        email = request.form['email']
        no_of_people = request.form['no_of_people']
        lat = request.form['lat']
        lng = request.form['lng']
        flat = request.form['flat']
        flong = request.form['flong']
        
        # Reload CSV to get updated data
        user_data = pd.read_csv("user_data.csv")
        user_row = user_data[user_data['email'] == email]

        selected = user_row[0]




if __name__ == "__main__":
    app.run(debug=True)