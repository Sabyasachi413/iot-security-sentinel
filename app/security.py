from app.models import IoTData

# Business Logic: Thresholds for Anomaly Detection
# These could eventually be moved to a config file or AI model
THRESHOLDS = {
    "max_data_kb": 2000.0,    # Anything above 2MB is suspicious
    "critical_data_kb": 10000.0, # 10MB is a major exfiltration event
    "temp_min": -40.0,
    "temp_max": 80.0
}

def analyze_telemetry(data: IoTData):
    """
    Core detection logic to identify threats.
    Returns: (is_anomaly: bool, severity: str, event_type: str, description: str)
    """
    
    # 1. Check for Data Exfiltration (Volume Anomaly)
    if data.data_size_kb > THRESHOLDS["critical_data_kb"]:
        return True, "CRITICAL", "Data Exfiltration", f"Massive outbound spike: {data.data_size_kb}KB"
    
    if data.data_size_kb > THRESHOLDS["max_data_kb"]:
        return True, "MEDIUM", "Unusual Traffic", f"High volume detected: {data.data_size_kb}KB"

    # 2. Check for Hardware Tampering (Sensor Anomaly)
    if data.temperature > THRESHOLDS["temp_max"] or data.temperature < THRESHOLDS["temp_min"]:
        return True, "HIGH", "Hardware Tamper", f"Impossible temperature: {data.temperature}C"

    # 3. Check for Unauthorized Firmware (Logic Anomaly)
    # If the firmware isn't a standard 'v1.x' or 'v2.x' format
    if not data.firmware_version.startswith("v"):
        return True, "LOW", "Unauthorized Firmware", f"Suspicious version string: {data.firmware_version}"

    return False, "NONE", "Normal", "Device operating within parameters"