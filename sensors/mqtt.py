import ssl
import os
import sys
import json
import time
import django


import paho.mqtt.client as mqtt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurae_monitoring.settings')
django.setup()

last_db_save_time = 0


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to EMQX Broker (Backend)")
    client.subscribe("Aurae_test_data_sensor")


def on_message(client, userdata, msg):
    global last_db_save_time
    current_time = time.time()

    try:
        # save every 1 hour
        if current_time - last_db_save_time >= 3600:
            from sensors.models import SensorReading
            payload = json.loads(msg.payload.decode('utf-8'))

            SensorReading.objects.create(
                temperature=payload.get('temperature'),
                humidity=payload.get('humidity'),
                pm25=payload.get('pm25'),
                co=payload.get('co')
            )
            print(f"Hourly Aurae data saved to PostgreSQL at {time.ctime()}")
            last_db_save_time = current_time

    except json.JSONDecodeError:
        print("Invalid JSON payload received")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message


client.username_pw_set("Esp-sensor-Trial", "12345678")

client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)

client.connect("c2717182.ala.eu-central-1.emqxsl.com", 8883, 60)

client.loop_forever()
