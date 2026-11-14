import time
import json
import random
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

# --- EMQX BROKER CONFIGURATION ---
# Replace with your EMQX IP, domain, or EMQX Cloud address
BROKER = "c2717182.ala.eu-central-1.emqxsl.com"
PORT = 8883               # Use 1883 for standard TCP, or 8883 for TLS/SSL
USE_TLS = True           # Set to True if using port 8883 (e.g., EMQX Cloud)
# Your EMQX Authentication username (if enabled)
USERNAME = "Esp-sensor-Trial"
# Your EMQX Authentication password (if enabled)
PASSWORD = "12345678"
INTERVAL_SECONDS = 30      # Publish interval in seconds

# All 48 Pangasinan ZIP codes
ZIP_CODES = [
    2408, 2415, 2404, 2425, 2405, 2439, 2442, 2407,
    2422, 2424, 2423, 2436, 2417, 2406, 2416, 2410,
    2418, 2400, 2411, 2412, 2402, 2437, 2401, 2409,
    2421, 2430, 2432, 2413, 2429, 2446, 2435, 2441,
    2420, 2433, 2431, 2438, 2447, 2444, 2419, 2440,
    2426, 2434, 2403, 2445, 2443, 2414, 2428, 2427
]


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected successfully to EMQX at {BROKER}:{PORT}")
    else:
        print(f"Connection failed with reason code: {reason_code}")


def generate_payload(zip_code):
    return {
        "device_id": zip_code,
        "temperature": round(random.uniform(26.0, 35.0), 1),
        "humidity": round(random.uniform(55.0, 80.0), 1),
        "pm25": round(random.uniform(10.0, 45.0), 1),
        "o3": round(random.uniform(0.01, 0.08), 2),
        "pm10": round(random.uniform(15.0, 60.0), 1),
        "nox": round(random.uniform(0.01, 0.05), 2),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                         client_id="aurae-emqx-48zip-bot")
    client.on_connect = on_connect

    if USERNAME and PASSWORD:
        client.username_pw_set(USERNAME, PASSWORD)

    if USE_TLS:
        client.tls_set()

    print(f"Connecting to EMQX ({BROKER}:{PORT})...")
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    try:
        while True:
            for zip_code in ZIP_CODES:
                topic = f"Aurae_test_data_sensor/{zip_code}"
                payload = json.dumps(generate_payload(zip_code))
                client.publish(topic, payload, qos=0)

            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] Sent 48 messages to Aurae_test_data_sensor/<zip>")
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nStopping EMQX simulator...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
