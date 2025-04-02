import subprocess
import psutil
import logging
import time
from pywinauto import Application
import pyautogui
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

# Constants
WINDOW_TITLE = "BlueStacks App Player"
STORE_TITLE   = r"BlueStacks Store"
PACK_NAME  = r"com.elnimr.haganboy"

APK_PATH        = r"D:\a\master\master\downloads\Haganboy.apk"
INSTALL_PATH    = r"D:\a\master\master\downloads\blue.exe"
HD_PLAYER_EXE   = r"C:\Program Files\BlueStacks_nxt\HD-Player.exe"


LUNCH_X_POSITION = 785
LUNCH_Y_POSITION = 545

DURATION_EXTRACT = 60
DURATION_INSTALL = 4
DURATION_LUNCH   = 180

CONFIRM_X = 822
CONFIRM_Y = 379


def click(x, y, duration):
    """Simulates a mouse click at (x, y) after a delay."""
    try:
        time.sleep(duration)
        pyautogui.click(x, y)
        logging.info(f"Clicked at ({x}, {y}) after {duration} seconds.")
        return True
    except Exception as e:
        logging.error(f"Click failed: {e}")
        return False


def setup():
    """Starts BlueStacks setup and launches the instance with proper logging and click simulation."""
    logging.info("Starting BlueStacks setup...")

    command = [
        INSTALL_PATH,
        "--defaultImageName", "Tiramisu64",
        "--imageToLaunch", "Tiramisu64"
    ]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info("Setup process started successfully.")

        logging.info("Application extracting...")
        click(LUNCH_X_POSITION, LUNCH_Y_POSITION, DURATION_EXTRACT)

        logging.info("Application installing...")
        click(LUNCH_X_POSITION, LUNCH_Y_POSITION, DURATION_INSTALL)

        logging.info("Application launching...")
        click(LUNCH_X_POSITION, LUNCH_Y_POSITION, DURATION_LUNCH)

        logging.info("Application launched successfully.")

        time.sleep(10) 
        terminate(STORE_TITLE)
        logging.info(f"{STORE_TITLE} launched successfully.")
        return True

    except Exception as e:
        logging.error(f"Setup failed: {e}")
        return False


def get_process_pid_by_title(title):
    """Retrieve the PID of a process by its window title."""
    try:
        app = Application(backend="win32").connect(title=title, timeout=10)
        return app.process
    except Exception as e:
        logging.error(f"Could not find process with title '{title}': {e}")
        return None


def is_process_running(pid):
    """Check if a process is still running."""
    return any(proc.pid == pid for proc in psutil.process_iter(attrs=['pid']))


def terminate(title):
    """Attempts to terminate a process by window title and verifies its termination."""
    logging.info(f"Attempting to terminate process with title: {title}")
    pid = get_process_pid_by_title(title)
    if not pid:
        logging.warning(f"No process found with title '{title}'.")
        return False
    try:
        app = Application(backend="win32").connect(process=pid)
        app.kill()
        logging.info(f"Process with PID {pid} terminated.")
        time.sleep(2)
        return not is_process_running(pid)
    except Exception as e:
        logging.error(f"Process termination failed: {e}")
        return False


def is_process_running_by_path(exe_path):
    """Check if a process is running based on its executable path."""
    for proc in psutil.process_iter(attrs=['pid', 'exe']):
        try:
            if proc.info['exe'] and proc.info['exe'].lower() == exe_path.lower():
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None


def start_process(exe_path):
    """Starts a process and verifies if it launched successfully."""
    logging.info(f"Attempting to start process: {exe_path}")
    if is_process_running_by_path(exe_path):
        logging.warning(f"Process 
