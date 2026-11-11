
import datetime
import pandas as pd
import requests
import threading
import time
import json
import ssl
import django
import os
import sys
from django.conf import settings
import paho.mqtt.client as mqtt


# 1. Configure Django environment and path FIRST before anything else
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurae_monitoring.settings')

# 2. Initialize Django setup
django.setup()


# Thread-safe lock for the message buffer
buffer_lock = threading.Lock()
message_buffer = []
FLUSH_INTERVAL = 3600  # 1 hour in seconds


try:
    import io
    import joblib
    from .models import SavedModel
    saved_record = SavedModel.objects.get(model_name='tuned_random_forest')

    model_bytes = io.BytesIO(bytes(saved_record.model_data))

    ml_models = joblib.load(model_bytes)
    ml_classifier = ml_models.get('classifier')
    ml_regressor = ml_models.get('regressor')
    scaler = ml_models.get('scaler')
    print("ML Models & Scaler loaded successfully from dictionary!")
except Exception as e:
    ml_classifier = None
    ml_regressor = None
    scaler = None
    print(f"Warning: Could not load ML models: {e}")


def flush_buffer_to_db():
    """Periodically flush the message buffer to the database every hour."""
    global message_buffer
    from django.db import connections
    from sensors.models import SensorReading

    connections.close_all()

    with buffer_lock:
        if not message_buffer:
            print(f"Hourly check: No messages received in the last hour.")
            return

        records_to_save = list(message_buffer)
        message_buffer.clear()

    try:
        SensorReading.objects.bulk_create(records_to_save)
        print(
            f"Saved {len(records_to_save)} records to PostgreSQL at {time.ctime()}")
    except Exception as e:
        print(f"Failed to write bulk data to PostgreSQL: {e}")


def schedule_periodic_flush():
    """Runs a background loop to flush the buffer hourly."""
    while True:
        time.sleep(FLUSH_INTERVAL)
        flush_buffer_to_db()


def notify_frontend(payload_data):
    """Sends real-time prediction data to the frontend via HTTP POST webhook/API."""
    from django.conf import settings
    frontend_url = getattr(settings, 'FRONTEND_WEBHOOK_URL',
                           'http://localhost:3000/api/sensor-stream')
    try:
        response = requests.post(frontend_url, json=payload_data, timeout=3)
        if response.status_code != 200:
            print(f"Failed to notify frontend: Status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP request to frontend failed: {e}")


def on_connect(client, userdata, flags, reason_code, properties):
    from django.conf import settings
    print(
        f"Connected to EMQX Broker (Backend) \n Topic: {settings.MQTT_TOPIC}")
    client.subscribe(settings.MQTT_TOPIC)


def on_message(client, userdata, msg):
    global message_buffer
    from sensors.models import SensorReading

    # Ignore messages that were already processed and published to avoid infinite loops
    if msg.topic.endswith('/processed'):
        return

    try:
        payload = json.loads(msg.payload.decode('utf-8'))

        # Extract device identifier (supports both payload field and topic structure)
        device_id = payload.get('device_id')
        if not device_id:
            # Fallback: Extract from topic e.g. Aurae_test_data_sensor/DeviceName
            topic_parts = msg.topic.split('/')
            if len(topic_parts) > 1:
                device_id = topic_parts[1]

        if not device_id:
            print("Error: Received message without a valid device_id.")
            return

        pm25 = float(payload.get('pm2.5', payload.get('pm25', 0.0)))
        pm10 = float(payload.get('pm10', 0.0))
        co = float(payload.get('co', 0.0))
        o3 = float(payload.get('o3', 0.0))
        nox = float(payload.get('nox', 0.0))

        # 1. Temporal features
        now = datetime.datetime.now()
        current_month = now.month
        current_day_of_week = now.weekday()

        # 2. Fetch past PM2.5 values isolated specifically to THIS device_id
        past_values = SensorReading.objects.filter(zipcode=device_id).order_by(
            '-timestamp').values_list('pm25', flat=True)[:6]

        history_pm25 = list(past_values)[::-1]  # Oldest to newest
        history_pm25.append(pm25)  # Append current reading

        # Convert to pandas Series for shift/rolling calculations
        s = pd.Series(history_pm25)

        pm25_lag_1 = float(s.shift(1).iloc[-1]) if len(s) >= 2 else pm25
        pm25_lag_2 = float(s.shift(2).iloc[-1]) if len(s) >= 3 else pm25_lag_1
        pm25_rolling_7day = float(s.rolling(window=7).mean().iloc[-1])

        predicted_aqi = None
        classification = "Unknown"

        # 3. Construct the 10-feature array
        features = [[
            pm25,
            pm10,
            co,
            o3,
            nox,
            pm25_lag_1,
            pm25_lag_2,
            pm25_rolling_7day,
            current_month,
            current_day_of_week
        ]]

        # Apply the loaded scaler so inputs match training dimensions
        if scaler is not None:
            model_input = scaler.transform(features)
        else:
            model_input = features

        # Run predictions using the scaled input
        if ml_regressor:
            aqi_pred = ml_regressor.predict(model_input)
            predicted_aqi = round(float(aqi_pred[0]), 2)

        if ml_classifier:
            cls_pred = ml_classifier.predict(model_input)
            try:
                raw_class = int(cls_pred[0])
                status_mapping = {
                    0: "Good",
                    1: "Fair",
                    2: "Unhealthy for Sensitive Groups",
                    3: "Very Unhealthy",
                    4: "Acutely Unhealthy (Local suspension discretion / shifting to distance learning)",
                    5: "Emergency (Automatic suspension of classes and work)"
                }
                classification = status_mapping.get(
                    raw_class, str(cls_pred[0]))
            except (ValueError, TypeError):
                classification = str(cls_pred[0])

        # Create model instance for database buffering
        reading = SensorReading(
            zipcode_id=device_id,
            temperature=float(payload.get('temperature', 0.0)),
            humidity=float(payload.get('humidity', 0.0)),
            pm25=pm25,
            co=co,
            no2=nox,
            aqi=predicted_aqi,
            classification=classification
        )

        with buffer_lock:
            message_buffer.append(reading)

        # Prepare payload for real-time frontend display
        realtime_payload = {
            "device_id": device_id,
            "temperature": payload.get('temperature', 0.0),
            "humidity": payload.get('humidity', 0.0),
            "pm25": pm25,
            "pm10": pm10,
            "o3": o3,
            "no2": nox,
            "aqi": predicted_aqi,
            "classification": classification,
            "timestamp": time.time()
        }

        # Publish uniquely to this device's corresponding processed topic
        processed_topic = f"Aurae_test_data_sensor/{device_id}/processed"
        client.publish(processed_topic, json.dumps(realtime_payload))
        print(
            f"Processed and published prediction for device: {device_id} -> {processed_topic}")

    except json.JSONDecodeError:
        print(f"Invalid JSON payload received on topic {msg.topic}")
    except Exception as e:
        print(
            f"Error processing message & running ML prediction for device: {e}")


def run_mqtt_listener():
    from django.conf import settings

    # Start the periodic background flushing thread for hourly database saves
    flush_thread = threading.Thread(
        target=schedule_periodic_flush, daemon=True)
    flush_thread.start()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, 60)
    client.loop_forever()


if __name__ == '__main__':
    run_mqtt_listener()
