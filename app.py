from flask import Flask, request, render_template
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model, scaler, and label encoders
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Identify categorical, boolean, and numerical columns
categorical_cols = ['region_code', 'segment', 'model', 'fuel_type', 'engine_type', 
                    'rear_brakes_type', 'transmission_type', 'steering_type']
boolean_cols = [col for col in ['is_esc', 'is_adjustable_steering', 'is_tpms', 'is_parking_sensors',
                                'is_parking_camera', 'is_front_fog_lights', 'is_rear_window_wiper',
                                'is_rear_window_washer', 'is_rear_window_defogger', 'is_brake_assist',
                                'is_power_door_locks', 'is_central_locking', 'is_power_steering',
                                'is_driver_seat_height_adjustable', 'is_day_night_rear_view_mirror',
                                'is_ecw', 'is_speed_alert']]
numerical_cols = ['subscription_length', 'vehicle_age', 'customer_age', 'region_density',
                  'displacement', 'cylinder', 'turning_radius', 'length', 'width',
                  'gross_weight', 'ncap_rating']

# Define a function for prediction
def predict_claim_status(input_data):
    # Encode categorical and boolean columns
    for col in categorical_cols + boolean_cols:
        le = label_encoders[col]
        if input_data[col] not in le.classes_:
            le.classes_ = np.append(le.classes_, input_data[col])
        input_data[col] = le.transform([input_data[col]])[0]
    
    # Collect numerical data
    numerical_data = [input_data[col] for col in numerical_cols]
    numerical_data = scaler.transform([numerical_data])[0]
    
    # Combine all data
    encoded_data = [input_data[col] for col in categorical_cols + boolean_cols]
    encoded_data.extend(numerical_data)
    
    # Convert input data to DataFrame
    input_df = pd.DataFrame([encoded_data], columns=categorical_cols + boolean_cols + numerical_cols)

    # Predict claim status
    prediction = model.predict(input_df)
    return prediction[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.form.to_dict()
    
    # Convert appropriate fields to numeric
    for col in numerical_cols:
        input_data[col] = float(input_data[col])
    
    prediction = predict_claim_status(input_data)
    result = 'Approved' if prediction == 1 else 'Rejected'
    return render_template('index.html', prediction_text=f'Claim Status: {result}')

if __name__ == "__main__":
    app.run(debug=True)
