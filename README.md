# 🛡️ IoT Security Sentinel (V1.0)
**An Adaptive Intrusion Detection Framework for Resource-Constrained WSNs.**

### 📊 Business Value
Traditional security suites are too heavy for IoT. **Sentinel** provides a lightweight, asynchronous middleware that validates telemetry in <50ms, preventing data exfiltration before it hits the cloud.

### 🏗️ Architecture
* **High-Speed API:** FastAPI & Pydantic for sub-millisecond validation.
* **Forensic Audit Log:** Structured SQL (SQLite) for incident response.
* **Live SOC Dashboard:** Real-time threat visualization via Jinja2 & Tailwind.

### 🛡️ Detection Capabilities
1. **Volume Spikes:** Identifies unauthorized data exfiltration (>10MB/s).
2. **Hardware Integrity:** Flags impossible sensor readings (Tamper detection).
3. **Logic Validation:** Rejects unauthorized firmware signatures.

---
*Developed by Sabyasachi | Lead Technical Consultant @ Apex Dev Solutions*