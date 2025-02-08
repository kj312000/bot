import subprocess

scripts = [
    'script1.py',
    'script2.py',
    'script3.py',
    'script4.py',
    'script5.py',
    'script6.py',
    'script7.py',
    'script8.py'
]

for script in scripts:
    try:
        subprocess.run(['python', script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script}: {e}")