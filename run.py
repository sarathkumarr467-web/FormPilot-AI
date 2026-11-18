"""
FormPilot AI — Quick Launcher (run.py).
"""
import os
import sys

current_dir = os.path.abspath(os.path.dirname(__file__))
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("=" * 70)
    print("      🚀 FORMPILOT AI — INTELLIGENT APPLICATION ASSISTANCE")
    print("      Tagline: Understand. Fill. Verify. Apply.")
    print("=" * 70)
    print(f"  * Web Application (UI) : http://127.0.0.1:{port}")
    print(f"  * API Documentation    : http://127.0.0.1:{port}/docs")
    print("=" * 70)

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=port,
        log_level="info"
    )
