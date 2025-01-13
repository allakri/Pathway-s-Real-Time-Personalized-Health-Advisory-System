
import random
import pandas as pd
from datetime import datetime

# Health metrics as per the user's input
health_metrics = [
    {"id": 1, "name": "Heart Rate", "unit": "bpm", "description": "Measures the number of heartbeats per minute."},
    {"id": 2, "name": "Blood Pressure", "unit": "mmHg", "description": "Tracks systolic and diastolic blood pressure levels."},
    {"id": 3, "name": "Blood Oxygen Level", "unit": "%", "description": "Measures the oxygen saturation in the blood."},
    {"id": 4, "name": "Respiratory Rate", "unit": "breaths/min", "description": "Tracks the number of breaths taken per minute."},
    {"id": 5, "name": "Body Temperature", "unit": "°C", "description": "Monitors body temperature to detect fever or hypothermia."},
    {"id": 6, "name": "ECG", "unit": "mV", "description": "Electrocardiogram to monitor heart's electrical activity."},
    {"id": 7, "name": "Sleep Quality", "unit": "score", "description": "Tracks sleep duration, stages, and quality."},
    {"id": 8, "name": "Stress Level", "unit": "score", "description": "Measures stress based on heart rate variability."},
    {"id": 9, "name": "Calories Burned", "unit": "kcal", "description": "Estimates the number of calories burned during activities."},
    {"id": 10, "name": "Steps Taken", "unit": "count", "description": "Counts the number of steps walked in a day."},
    {"id": 11, "name": "Distance Traveled", "unit": "km", "description": "Measures the distance covered while walking or running."},
    {"id": 12, "name": "Active Minutes", "unit": "minutes", "description": "Tracks the duration of physical activity."},
    {"id": 13, "name": "VO2 Max", "unit": "mL/kg/min", "description": "Estimates the maximum oxygen consumption during exercise."},
    {"id": 14, "name": "Heart Rate Variability", "unit": "ms", "description": "Measures variations in the time intervals between heartbeats."},
    {"id": 15, "name": "Hydration Level", "unit": "score", "description": "Tracks hydration based on activity and sweat loss."},
    {"id": 16, "name": "Body Fat Percentage", "unit": "%", "description": "Estimates body fat composition."},
    {"id": 17, "name": "Muscle Mass", "unit": "kg", "description": "Estimates the total muscle mass in the body."},
    {"id": 18, "name": "Skin Temperature", "unit": "°C", "description": "Monitors temperature changes on the skin surface."},
    {"id": 19, "name": "Energy Expenditure", "unit": "kcal", "description": "Estimates total daily energy expenditure."},
    {"id": 20, "name": "Recovery Time", "unit": "hours", "description": "Estimates the recovery time needed after exercise."}
]

# Function to generate random fake data
def generate_fake_data(timestamp):
    data = {"timestamp": timestamp}
    for metric in health_metrics:
        metric_data = {}
        metric_data["name"] = metric["name"]
        metric_data["unit"] = metric["unit"]
        
        # Generate fake values based on the type of metric
        if metric["unit"] == "bpm":
            metric_data["value"] = random.randint(50, 100)  # Heart rate, max 100 bpm
        elif metric["unit"] == "mmHg":
            metric_data["value"] = f"{random.randint(90, 140)}/{random.randint(60, 90)}"  # Blood pressure
        elif metric["unit"] == "%":
            metric_data["value"] = random.randint(95, 100)  # Blood Oxygen Level
        elif metric["unit"] == "breaths/min":
            metric_data["value"] = random.randint(12, 18)  # Respiratory rate
        elif metric["unit"] == "°C":
            metric_data["value"] = round(random.uniform(36.0, 37.5), 1)  # Body temperature
        elif metric["unit"] == "mV":
            metric_data["value"] = round(random.uniform(0.1, 1.5), 2)  # ECG
        elif metric["unit"] == "score":
            metric_data["value"] = random.randint(1, 10)  # Stress level, Sleep quality, etc.
        elif metric["unit"] == "kcal":
            metric_data["value"] = random.randint(100, 300)  # Calories burned
        elif metric["unit"] == "count":
            metric_data["value"] = random.randint(0, 10000)  # Steps taken
        elif metric["unit"] == "km":
            metric_data["value"] = round(random.uniform(0.0, 10.0), 2)  # Distance traveled
        elif metric["unit"] == "minutes":
            metric_data["value"] = random.randint(0, 120)  # Active minutes
        else:
            metric_data["value"] = "N/A"
        
        data[metric["name"]] = metric_data["value"]
    
    return data

# Collect data every 10 minutes for 100 entries
data_points = []
for i in range(100):  # 100 data points
    timestamp = (datetime.now() + pd.Timedelta(minutes=10*i)).strftime("%Y-%m-%d %H:%M:%S")
    data_points.append(generate_fake_data(timestamp))

# Convert data points to a pandas DataFrame
df = pd.DataFrame(data_points)

# Save the data to an Excel file
excel_file = "health_metrics_data_100_entries.xlsx"
df.to_excel(excel_file, index=False, engine='openpyxl')

print(f"Fake health metrics data has been saved to {excel_file}")
