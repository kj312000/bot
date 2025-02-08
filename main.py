import subprocess
from concurrent.futures import ThreadPoolExecutor

scripts = [
    'script1.py',
    'script2.py',
    'script3.py',
    'script4.py',
    'script5.py',
    'script6.py'
]

def run_script(script):
    try:
        print(f"Running {script}...")
        subprocess.run(['python', script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script}: {e}")

with ThreadPoolExecutor() as executor:
    # Execute the scripts in parallel
    executor.map(run_script, scripts)
