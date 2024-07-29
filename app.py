from flask import Flask, request, render_template, jsonify
import pandas as pd
import joblib
import numpy as np
import sqlite3
import datetime
import matplotlib.pyplot as plt
# plt.use('Agg')

import seaborn as sns
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

app = Flask(__name__)

# Load the trained model, scaler, and label encoders
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Define the columns
categorical_cols = ['region_code', 'segment', 'model', 'fuel_type', 'engine_type', 'rear_brakes_type', 'transmission_type', 'steering_type']
boolean_cols = ['is_esc', 'is_adjustable_steering', 'is_tpms', 'is_parking_sensors', 'is_parking_camera', 'is_front_fog_lights', 
                'is_rear_window_wiper', 'is_rear_window_washer', 'is_rear_window_defogger', 'is_brake_assist', 'is_power_door_locks', 
                'is_central_locking', 'is_power_steering', 'is_driver_seat_height_adjustable', 'is_day_night_rear_view_mirror', 'is_ecw', 
                'is_speed_alert']
numerical_cols = ['subscription_length', 'vehicle_age', 'customer_age', 'region_density', 'displacement', 'cylinder', 'turning_radius', 
                  'length', 'width', 'gross_weight', 'ncap_rating']

# Function to predict claim status
def predict_claim_status(input_data):
    for col in categorical_cols + boolean_cols:
        le = label_encoders[col]
        if input_data[col] not in le.classes_:
            le.classes_ = np.append(le.classes_, input_data[col])
        input_data[col] = le.transform([input_data[col]])[0]

    numerical_data = [input_data[col] for col in numerical_cols]
    numerical_data = scaler.transform([numerical_data])[0]

    encoded_data = [input_data[col] for col in categorical_cols + boolean_cols]
    encoded_data.extend(numerical_data)

    input_df = pd.DataFrame([encoded_data], columns=categorical_cols + boolean_cols + numerical_cols)

    prediction = model.predict(input_df)
    return prediction[0]

# Initialize the database
def init_db():
    conn = sqlite3.connect('claims.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS claims
                 (id INTEGER PRIMARY KEY, name TEXT, date TEXT, email TEXT, region_code TEXT, segment TEXT, model TEXT, 
                  fuel_type TEXT, engine_type TEXT, rear_brakes_type TEXT, transmission_type TEXT, steering_type TEXT, 
                  is_esc INTEGER, is_adjustable_steering INTEGER, is_tpms INTEGER, is_parking_sensors INTEGER, 
                  is_parking_camera INTEGER, is_front_fog_lights INTEGER, is_rear_window_wiper INTEGER, 
                  is_rear_window_washer INTEGER, is_rear_window_defogger INTEGER, is_brake_assist INTEGER, 
                  is_power_door_locks INTEGER, is_central_locking INTEGER, is_power_steering INTEGER, 
                  is_driver_seat_height_adjustable INTEGER, is_day_night_rear_view_mirror INTEGER, is_ecw INTEGER, 
                  is_speed_alert INTEGER, subscription_length REAL, vehicle_age REAL, customer_age REAL, 
                  region_density REAL, displacement REAL, cylinder REAL, turning_radius REAL, length REAL, width REAL, 
                  gross_weight REAL, ncap_rating REAL, claim_status TEXT)''')
    conn.commit()
    conn.close()

# Insert claim data into the database
def insert_claim_to_db(claim_data, claim_status):
    conn = sqlite3.connect('claims.db')
    c = conn.cursor()
    c.execute('''INSERT INTO claims (name, date, email, region_code, segment, model, fuel_type, engine_type, rear_brakes_type,
                 transmission_type, steering_type, is_esc, is_adjustable_steering, is_tpms, is_parking_sensors, 
                 is_parking_camera, is_front_fog_lights, is_rear_window_wiper, is_rear_window_washer, 
                 is_rear_window_defogger, is_brake_assist, is_power_door_locks, is_central_locking, is_power_steering, 
                 is_driver_seat_height_adjustable, is_day_night_rear_view_mirror, is_ecw, is_speed_alert, 
                 subscription_length, vehicle_age, customer_age, region_density, displacement, cylinder, turning_radius, 
                 length, width, gross_weight, ncap_rating, claim_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                 ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                 (claim_data['name'], claim_data['date'], claim_data['email'], claim_data['region_code'], claim_data['segment'], 
                  claim_data['model'], claim_data['fuel_type'], claim_data['engine_type'], claim_data['rear_brakes_type'], 
                  claim_data['transmission_type'], claim_data['steering_type'], claim_data['is_esc'], 
                  claim_data['is_adjustable_steering'], claim_data['is_tpms'], claim_data['is_parking_sensors'], 
                  claim_data['is_parking_camera'], claim_data['is_front_fog_lights'], claim_data['is_rear_window_wiper'], 
                  claim_data['is_rear_window_washer'], claim_data['is_rear_window_defogger'], claim_data['is_brake_assist'], 
                  claim_data['is_power_door_locks'], claim_data['is_central_locking'], claim_data['is_power_steering'], 
                  claim_data['is_driver_seat_height_adjustable'], claim_data['is_day_night_rear_view_mirror'], 
                  claim_data['is_ecw'], claim_data['is_speed_alert'], claim_data['subscription_length'], 
                  claim_data['vehicle_age'], claim_data['customer_age'], claim_data['region_density'], claim_data['displacement'], 
                  claim_data['cylinder'], claim_data['turning_radius'], claim_data['length'], claim_data['width'], 
                  claim_data['gross_weight'], claim_data['ncap_rating'], claim_status))
    conn.commit()
    conn.close()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.form.to_dict()
    input_data['date'] = datetime.datetime.now().strftime("%Y-%m-%d")

    for col in numerical_cols:
        input_data[col] = float(input_data[col])
    for col in boolean_cols:
        input_data[col] = int(input_data[col])

    prediction = predict_claim_status(input_data)
    result = 'Approved' if prediction == 1 else 'Rejected'
    input_data['claim_status'] = result

    insert_claim_to_db(input_data, result)

    return render_template('index.html', prediction_text=f'Claim Status: {result}')

@app.route('/visualization', methods=['GET'])
def visualization():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = sqlite3.connect('claims.db')
    df = pd.read_sql_query("SELECT date, claim_status FROM claims", conn)
    conn.close()

    df['date'] = pd.to_datetime(df['date'])
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    sns.set(style="darkgrid")
    plt.figure(figsize=(10, 6))
    chart1 = sns.countplot(x='date', hue='claim_status', data=df)
    plt.title('Claims Status by Date')
    chart1.figure.savefig('static/claims_by_date.png')

    plt.figure(figsize=(10, 6))
    chart2 = sns.countplot(x='claim_status', data=df)
    plt.title('Overall Claims Status')
    chart2.figure.savefig('static/overall_claims_status.png')

    return render_template('visualization.html')

@app.route('/data')
def data():
    conn = sqlite3.connect('claims.db')
    df = pd.read_sql_query("SELECT name, date, email, claim_status FROM claims", conn)
    conn.close()

    return render_template('data.html', data=df.to_html(index=False))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    input_data = request.get_json()

    for col in numerical_cols:
        input_data[col] = float(input_data[col])
    for col in boolean_cols:
        input_data[col] = int(input_data[col])

    prediction = predict_claim_status(input_data)
    result = 'Approved' if prediction == 1 else 'Rejected'

    return jsonify({'claim_status': result})

@app.route('/api/send_report', methods=['GET'])
def send_report():
    email = request.args.get('email')
    conn = sqlite3.connect('claims.db')
    df = pd.read_sql_query("SELECT date, claim_status FROM claims", conn)
    conn.close()

    sns.set(style="darkgrid")
    plt.figure(figsize=(10, 6))
    chart1 = sns.countplot(x='date', hue='claim_status', data=df)
    plt.title('Claims Status by Date')
    chart1.figure.savefig('static/claims_by_date.png')

    plt.figure(figsize=(10, 6))
    chart2 = sns.countplot(x='claim_status', data=df)
    plt.title('Overall Claims Status')
    chart2.figure.savefig('static/overall_claims_status.png')

    message = MIMEMultipart()
    message['From'] = 'grishma.renuka@gmail.com'
    message['To'] = email
    message['Subject'] = 'Claims Report'

    body = 'Attached is the claims report.'
    message.attach(MIMEText(body, 'plain'))

    filenames = ['static/claims_by_date.png', 'static/overall_claims_status.png']
    for filename in filenames:
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            message.attach(part)

    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login('grishma.renuka@gmail.com', 'Mani!@18')
    text = message.as_string()
    server.sendmail('grishma.renuka@gmail.com', email, text)
    server.quit()

    return jsonify({'message': 'Report sent successfully'})

@app.route('/api_integration')
def api_integration():
    return render_template('api_integration.html')

if __name__ == "__main__":
    init_db()
    app.run(debug=True, threaded=False)
