"""
FormPilot AI — Main Application Launcher.
Tagline: Understand. Fill. Verify. Apply.
Launches the full-stack FastAPI application and serves the bilingual Next.js/React frontend.
"""
import os
import sys

# Locate formpilot-ai directory dynamically
current_dir = os.path.abspath(os.path.dirname(__file__))

# If script is inside formpilot-ai, use current_dir; otherwise join
if os.path.basename(current_dir) == "formpilot-ai":
    project_dir = current_dir
else:
    project_dir = os.path.join(current_dir, "formpilot-ai")

backend_dir = os.path.join(project_dir, "backend")

if project_dir not in sys.path:
    sys.path.insert(0, project_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

os.chdir(project_dir)

import uvicorn
from backend.app.main import app
from backend.app.core.config import settings

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("=" * 70)
    print("      🚀 FORMPILOT AI — INTELLIGENT APPLICATION ASSISTANCE")
    print("      Tagline: Understand. Fill. Verify. Apply.")
    print("      INNOVATE INDIA Hackathon 2026")
    print("=" * 70)
    print(f"  * Web Application (UI) : http://127.0.0.1:{port}")
    print(f"  * API Documentation    : http://127.0.0.1:{port}/docs")
    print(f"  * Health Check         : http://127.0.0.1:{port}/api/health")
    print(f"  * ML Model Metrics     : http://127.0.0.1:{port}/api/ml/metrics")
    print("=" * 70)
    print("  Press Ctrl+C to stop the server.")
    print("=" * 70)

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=port,
        log_level="info"
    )
