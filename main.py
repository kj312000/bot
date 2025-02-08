import subprocess
from concurrent.futures import ThreadPoolExecutor
import logging
import time
from threading import Thread

# Set up logging
logging.basicConfig(level=logging.INFO)

# List of script names to run concurrently
scripts = [
    'script1.py',
    'script2.py',
    'script3.py',
    'script4.py',
    'script5.py',
    'script6.py'
]

# Function to run a script using subprocess.Popen (non-blocking)
def run_script(script):
    try:
        process = subprocess.Popen(['python', script])
        process.communicate()  # Wait for the script to complete
    except Exception as e:
        logging.error(f"Error occurred while running {script}: {e}")

# Function to keep the container alive with periodic heartbeat
def keep_alive():
    while True:
        logging.info("Heartbeat: Container is still active.")
        time.sleep(60)  # Sleep for 60 seconds before logging again

# Start the heartbeat function in a separate thread
keep_alive_thread = Thread(target=keep_alive)
keep_alive_thread.daemon = True  # Ensure it doesn't block the main program
keep_alive_thread.start()

# Main execution for running all scripts concurrently
with ThreadPoolExecutor() as executor:
    executor.map(run_script, scripts)
