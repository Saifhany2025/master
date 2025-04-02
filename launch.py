#launch.py
import subprocess

def start_proc(path="run.bat"):
    try:
        subprocess.Popen(path, shell=True)  # `shell=True` is required for .bat files
        return True
    except Exception as e:
        print(f"[-] start_proc : {e}")
        return False

start_proc()