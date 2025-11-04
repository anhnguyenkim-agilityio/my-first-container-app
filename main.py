from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Azure FastAPI Example",
    version="1.0.0",
    description="A sample FastAPI REST API running in a Docker container on Azure.",
)

# Configure CORS so the static web app (and local dev) can call the API
# from the browser. If you prefer to restrict origins, replace ['*']
# with e.g. ['https://your-static-site.azurestaticapps.net']
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/test", response_class=JSONResponse)
def test_endpoint():
    data = {
        "status": "success",
        "message": "Hello from Azure Dockerized API! - v1",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    return JSONResponse(content=data)


@app.get("/healthz", response_class=JSONResponse)
def health_check():
    """Simple health check endpoint for Azure probes."""
    data = {
        "status": "healthy",
        "service": "FastAPI Azure Example",
        "time": datetime.utcnow().isoformat() + "Z",
    }
    return JSONResponse(content=data)
