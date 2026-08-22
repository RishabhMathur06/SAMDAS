import os
import uvicorn

def run_dashboard():
    """
    Entry point for the 'samdas-dashboard' CLI command.
    Spins up the FastAPI server and serves the dashboard.
    """
    os.environ["SAMDAS_DASHBOARD_MODE"] = "1"

    print("starting SAMDAS Control Plane Dashboard...")
    uvicorn.run("samdas.server.main:app", host="127.0.0.1", port=8000, reload=True)