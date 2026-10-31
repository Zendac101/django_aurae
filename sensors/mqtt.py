from django.conf import settings  # isort: skip
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


def run_mqtt_listener():

    # mqtt login
    from django.conf import settings

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

    client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, 60)

    client.loop_forever()


message_buffer = []

last_db_save_time = time.time()


def on_connect(client, userdata, flags, reason_code, properties):
    from django.conf import settings

    print(
        f"Connected to EMQX Broker (Backend) \n Topic: {settings.MQTT_TOPIC}")
    client.subscribe(settings.MQTT_TOPIC)


def on_message(client, userdata, msg):
    global last_db_save_time, message_buffer
    current_time = time.time()

    try:

        payload = json.loads(msg.payload.decode('utf-8'))

        from sensors.models import SensorReading

        reading = SensorReading(
            zipcode_id=payload.get('device_id'),
            temperature=payload.get('temperature'),
            humidity=payload.get('humidity'),
            pm25=payload.get('pm25'),
            co=payload.get('co'),
        )
        message_buffer.append(reading)

    except json.JSONDecodeError:
        print(f"Invalid JSON payload received on topic {msg.topic}")

    if current_time - last_db_save_time >= 3600:
        try:
            if message_buffer:

                SensorReading.objects.bulk_create(message_buffer)
                print(
                    f"Saved {len(message_buffer)} records to PostgreSQL at {time.ctime()}"
                )

                message_buffer.clear()
            else:
                print(f"Hourly check: No messages received in the last hour.")

        except Exception as e:
            print(f"Failed to write bulk data to PostgreSQL: {e}")

        last_db_save_time = current_time


# run the client login
if __name__ == '__main__':
    run_mqtt_listener()
