import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Internal Project Imports
from app.models import IoTData
from app.security import analyze_telemetry
from app.database import init_db, log_security_event, get_all_alerts
from app.logger import logger

app = FastAPI(title="IoT Security Sentinel")

# --- ASSET PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=template_path)

# --- STARTUP SEQUENCE ---
@app.on_event("startup")
def startup_event():
    init_db()
    logger.info("🚀 SENTINEL SYSTEM ONLINE: Database and Security Engine Initialized.")

@app.get("/")
def read_root():
    return {"status": "Sentinel Active", "version": "1.0.0", "dashboard": "/dashboard"}

# --- THE TELEMETRY GATEWAY ---
@app.post("/telemetry")
async def receive_telemetry(data: IoTData):
    """Receives IoT data, logs the hit, and runs the Security Engine."""
    
    # 1. Immediate Log (Visibility)
    logger.info(f"📥 INBOUND: Device={data.device_id} | Data={data.data_size_kb}KB | Temp={data.temperature}C")

    # 2. Run Anomaly Detection
    is_anomaly, severity, event_type, description = analyze_telemetry(data)
    
    # 3. Action Logic
    if is_anomaly:
        logger.warning(f"🚨 ALERT: {severity} {event_type} detected on {data.device_id}!")
        
        log_security_event(
            device_id=data.device_id,
            event_type=event_type,
            severity=severity,
            description=description
        )
        return {
            "status": "FLAGGED",
            "threat_level": severity,
            "message": description
        }
    
    return {"status": "SECURE", "message": "Telemetry verified."}

# --- THE LIVE DASHBOARD ---
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """Renders the Real-time Security Operations Center (SOC) Dashboard."""
    try:
        # Fetch alerts from SQL
        alerts_data = get_all_alerts()
        
        logger.info(f"🖥️ DASHBOARD ACCESS: Displaying {len(alerts_data)} security events.")
        
        # Explicitly passing 'request' and 'context' for modern FastAPI compatibility
        return templates.TemplateResponse(
            request=request, 
            name="dashboard.html", 
            context={"alerts": alerts_data}
        )
        
    except Exception as e:
        logger.error(f"❌ DASHBOARD FAILURE: {str(e)}")
        return HTMLResponse(content=f"<h1>Dashboard Error</h1><p>{str(e)}</p>", status_code=500)

# --- API DEBUG ENDPOINT ---
@app.get("/api/alerts")
def view_alerts_json():
    """Returns the raw JSON of all logged threats."""
    alerts = get_all_alerts()
    return {"count": len(alerts), "alerts": alerts}