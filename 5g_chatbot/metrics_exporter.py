from fastapi import FastAPI
import subprocess

app = FastAPI()

def get_ueransim_metrics():
    """Simulates collecting metrics from UERANSIM logs."""
    gnb_status = subprocess.getoutput("pgrep -f nr-gnb | wc -l")
    ue_status = subprocess.getoutput("pgrep -f nr-ue | wc -l")
    
    return {
        "gnb_active": int(gnb_status),
        "ue_active": int(ue_status)
    }

@app.get("/metrics")
def metrics():
    return get_ueransim_metrics()
