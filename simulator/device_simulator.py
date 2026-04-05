import requests
import time
from datetime import datetime
import random

# The URL of our FastAPI Sentinel (running in Terminal 1)
API_URL = "http://127.0.0.1:8000/telemetry"

def send_telemetry(device_id, data_size, temp, firmware):
    """Sends a single JSON payload to the Sentinel API."""
    payload = {
        "device_id": device_id,
        "timestamp": datetime.now().isoformat(),
        "data_size_kb": data_size,
        "temperature": temp,
        "firmware_version": firmware,
        "metadata": {"location": "West-Bengal-Zone-1"}
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()
        print(f"📡 [{device_id}] Status: {result['status']} | Msg: {result['message']}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def start_simulation():
    print("🚀 IoT Simulation Started. Press Ctrl+C to stop.\n")
    
    devices = ["smart-lock-01", "thermostat-04", "security-cam-09"]
    
    while True:
        for dev in devices:
            # --- NORMAL TRAFFIC ---
            # Most of the time, devices send small, safe packets
            send_telemetry(dev, random.uniform(0.5, 5.0), 22.5, "v1.0.4")
            
            # --- TRIGGER: DATA EXFILTRATION (CRITICAL) ---
            if random.random() < 0.1: # 10% chance
                print("\n🔥 [ATTACK] Simulating massive data spike from Camera...")
                send_telemetry("security-cam-09", 15000.0, 30.0, "v1.0.4")
            
            # --- TRIGGER: HARDWARE TAMPER (HIGH) ---
            if random.random() < 0.05: # 5% chance
                print("\n🌡️ [ATTACK] Simulating impossible temperature on Thermostat...")
                send_telemetry("thermostat-04", 1.2, 999.0, "v1.0.4")
                
            # --- TRIGGER: MALICIOUS FIRMWARE (LOW) ---
            if random.random() < 0.05:
                print("\n👾 [ATTACK] Simulating unauthorized firmware string...")
                send_telemetry(dev, 2.0, 20.0, "HACKED_BY_X")

            time.sleep(3) # Wait 3 seconds between device pings

if __name__ == "__main__":
    start_simulation()