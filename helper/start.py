import os
import subprocess

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(parent_dir, "frontend")
backend_dir = os.path.join(parent_dir, "backend")

def start_server():
    """Start FastAPI server with auto-reload for backend changes only."""
    try:
        print("Starting the FastAPI Server....")
        return subprocess.Popen(
            ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001", "--reload", "--reload-dir", backend_dir ], 
            cwd=backend_dir
        )

    except Exception as e:
        print(f"Error starting FastAPI server: {e}")
        return None

def start_ui():
    """Start Streamlit app with auto-reload for frontend changes only."""
    try:
        ui_script = os.path.join(frontend_dir, "ui.py")
        print("Starting the Streamlit Server....")
        return subprocess.Popen(["streamlit", "run", ui_script], cwd=frontend_dir)  # Reload only for frontend files

    except Exception as e:
        print(f"Error starting Streamlit UI: {e}")
        return None


def start_all():
    """Start all processes and manage shutdown."""
    server_process = start_server()
    ui_process = start_ui()

    if not server_process or not ui_process:
        print("One or more processes failed to start. Exiting...")
        exit(1)

    try:
        server_process.wait()
        ui_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down gracefully....")
        if server_process:
            server_process.terminate()
        if ui_process:
            ui_process.terminate()
