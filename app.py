import argparse
import subprocess
import sys
from src.dev_pilot.api.fastapi_app import load_app as load_fastapi_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch DevPilot in a specific mode.")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["fastapi", "streamlit"],
        required=True,
        help="Mode to run the application. Use 'fastapi' for the FastAPI server, or 'streamlit' for the Streamlit UI."
    )
    args = parser.parse_args()

    if args.mode == "fastapi":
        load_fastapi_app()
    elif args.mode == "streamlit":
        # Use subprocess to invoke the Streamlit CLI
        subprocess.run([sys.executable, "-m", "streamlit", "run", "src/dev_pilot/ui/streamlit_ui/streamlit_app.py"])