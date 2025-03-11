
import os
import subprocess
import sys
from threading import Thread

def run_streamlit():
    """Run the Streamlit application in a separate thread."""
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "app.py", "--server.port=8502", 
        "--server.address=0.0.0.0", 
        "--server.headless=true"
    ])

# This thread will start the Streamlit application
streamlit_thread = Thread(target=run_streamlit)
streamlit_thread.daemon = True
streamlit_thread.start()

# A simple WSGI application that proxies requests to Streamlit
def application(environ, start_response):
    """WSGI application that forwards to the Streamlit server."""
    # Streamlit will handle requests on its own port
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Streamlit application is running. Please access it on the correct port."]
