import time
from adb_shell.adb_device import AdbDeviceTcp
import re
import xml.etree.ElementTree as ET
device = None  

# -----------------------------------------------
# ✅ ADB Device Connection with Retry
# -----------------------------------------------

def connect(host="127.0.0.1", port=5555, max_retries=3):
    global device
    """Connect to BlueStacks via ADB with retry mechanism."""
    device = AdbDeviceTcp(host, port)  # Use AdbDeviceTcp instead of AdbDevice
    for attempt in range(max_retries):
        try:
            device.connect()
            if device.available:
                print(f"[+] Connected to BlueStacks (Attempt {attempt+1})")
                device2 = device 
                return device
        except Exception as e:
            print(f"[-] ADB Connection failed (Attempt {attempt+1}): {e}")
        time.sleep(3)
    
    print("[-] Failed to connect to BlueStacks after multiple attempts.")
    return None

# -----------------------------------------------
# ✅ Install & Uninstall APKs
# -----------------------------------------------


def is_app_installed(package_name):
    global device

    if not device:
        print("[-] No ADB device connected.")
        return False

    try:
        output = device.shell("pm list packages")
        installed_packages = output.split("\n")
        return any(f"package:{package_name}" in pkg for pkg in installed_packages)
    except Exception as e:
        print(f"[-] is_app_installed Error: {e}")
        return False


def install_apk(apk_path, package_name):
    global device
    if not device:
        return "ADB connection failed."

    if is_app_installed(package_name):
        print(f"[+] {package_name} is already installed.")
        return "Already Installed"

    bluestacks_apk_path = "/data/local/tmp/Haganboy.apk"  # Path inside BlueStacks

    try:
        print(f"[+] Pushing APK to BlueStacks...")
        device.push(apk_path, bluestacks_apk_path)  # ✅ Pass file path, not file object

        print(f"[+] Installing APK from {bluestacks_apk_path}...")
        install_output = device.shell(f"pm install -r {bluestacks_apk_path}")

        print(f"[+] Install output: {install_output}")
        return install_output
    except Exception as e:
        print(f"[-] Install error: {e}")
        return f"[-] Install error: {e}"


def uninstall_apk(package_name):
    """Uninstall an app from BlueStacks."""
    device = connect_adb()
    if not device:
        return "ADB connection failed."

    try:
        uninstall_output = device.shell(f"pm uninstall {package_name}")
        print(f"[+] Uninstalled {package_name}")
        return uninstall_output
    except Exception as e:
        return f"[-] Uninstall Error: {e}"


def is_app_fully_loaded_2(package_name, timeout=30):
    global device
    if not device:
        return False

    print(f"[+] Waiting for {package_name} to fully load...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Get the currently running foreground activity
            output = device.shell("dumpsys activity activities | grep mResumedActivity")
            if package_name in output:
                print(f"[✅] {package_name} is fully loaded and in foreground.")
                return True
        except Exception as e:
            print(f"[-] Error checking app status: {e}")

        time.sleep(1)  # Wait and check again

    print(f"[-] Timeout: {package_name} did not fully load in {timeout} seconds.")
    return False


def is_app_fully_loaded(package_name, timeout=30):
    """Waits until an app is fully loaded by checking window focus and process ID."""
    global device
    if not device:
        return False

    print(f"[+] Waiting for {package_name} to fully load...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Step 1: Check if app is in the foreground
            foreground_output = device.shell("dumps
