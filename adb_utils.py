import time
from adb_shell.adb_device import AdbDeviceTcp
import re
import xml.etree.ElementTree as ET
device = None  


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
            foreground_output = device.shell("dumpsys window | grep mCurrentFocus")
            if package_name in foreground_output:
                print(f"[✅] {package_name} is in the foreground.")

            # Step 2: Check if app process is running
            process_output = device.shell(f"pidof {package_name}")
            if process_output.strip():
                print(f"[✅] {package_name} process is active.")

            # If both conditions are met, app is fully loaded
            if package_name in foreground_output and process_output.strip():
                print(f"[🎉] {package_name} is fully loaded!")
                return True

        except Exception as e:
            print(f"[-] Error checking app status: {e}")

        time.sleep(1)  # Wait before checking again

    print(f"[-] Timeout: {package_name} did not fully load in {timeout} seconds.")
    return False


def is_app_fully_loaded_window(package_name, timeout=30):
    """Waits until an app is fully loaded by checking top window activity."""
    global device
    if not device:
        return False

    print(f"[+] Waiting for {package_name} to be in the foreground...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            output = device.shell("dumpsys window windows | grep mCurrentFocus")
            
            if package_name in output:
                print(f"[✅] {package_name} is fully loaded and in focus!")
                return True

        except Exception as e:
            print(f"[-] Error checking window focus: {e}")

        time.sleep(1)  

    print(f"[-] Timeout: {package_name} did not fully load in {timeout} seconds.")
    return False


def launch_app(package_name):
    global device
    if not device:
        return "ADB connection failed."

    try:
        device.shell(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
        print(f"[+] Launched {package_name} successfully!")
    except Exception as e:
        print(f"[-] Failed to launch {package_name}: {e}")


def terminate_app(package_name):
    global device
    if not device:
        return "ADB connection failed."

    try:
        print(f"[+] Terminating {package_name}...")
        device.shell(f"am force-stop {package_name}")  # Force stop the app
        print(f"[+] {package_name} has been terminated.")
        return True
    except Exception as e:
        print(f"[-] Error terminating app: {e}")
        return False


def is_app_running(package_name):
    global device
    if not device:
        return False
    try:
        output = device.shell(f"pidof {package_name}")  # Get process ID
        return bool(output.strip())  # If output is not empty, the app is running
    except Exception as e:
        print(f"[-] Error checking if app is running: {e}")
        return False


def is_app_running_ps(package_name):
    """Alternative method using `ps` command to check if an app is running."""
    global device
    if not device:
        return False

    try:
        output = device.shell("ps | grep " + package_name)
        return package_name in output  # If found, app is running
    except Exception as e:
        print(f"[-] Error checking app process: {e}")
        return False
    

def get_running_app():
    global device
    if not device:
        print("[-] ADB connection failed.")
        return None

    try:
        # Get the list of running activities
        output = device.shell("dumpsys activity activities")

        # Debugging: Print raw output
        #print(f"[+] Raw ADB Output:\n{output}")

        # Look for the focused activity
        for line in output.splitlines():
            if "mResumedActivity" in line or "topResumedActivity" in line:
                #print(f"[+] Matched Line: {line}")  # Debugging output
                package_name = line.split()[2].split("/")[0]  # Extract package name
                print(f"[+] Current running app: {package_name}")
                return package_name

        print("[-] Could not determine the running app.")
        return None
    except Exception as e:
        print(f"[-] Error getting running app: {e}")
        return None



def launch_play_store():
    global device
    if not device:
        print("[-] ADB connection failed.")
        return False

    try:
        print("[+] Launching Google Play Store...")
        device.shell("monkey -p com.android.vending -c android.intent.category.LAUNCHER 1")
        print("[+] Google Play Store launched successfully!")
        return True
    except Exception as e:
        print(f"[-] Error launching Play Store: {e}")
        return False
    

def change_device_profile(manufacturer="Samsung", brand="Galaxy", model="S23"):
    global device
    if not device:
        print("[-] ADB connection failed.")
        return False

    try:
        print(f"[+] Changing device profile:")
        print(f"    📌 Manufacturer: {manufacturer}")
        print(f"    📌 Brand: {brand}")
        print(f"    📌 Model: {model}")

        # Apply changes using ADB shell properties
        device.shell(f"setprop ro.product.manufacturer \"{manufacturer}\"")
        device.shell(f"setprop ro.product.brand \"{brand}\"")
        device.shell(f"setprop ro.product.model \"{model}\"")

        # Verify changes
        new_manufacturer = device.shell("getprop ro.product.manufacturer").strip()
        new_brand = device.shell("getprop ro.product.brand").strip()
        new_model = device.shell("getprop ro.product.model").strip()

        print(f"[✅] New Manufacturer: {new_manufacturer}")
        print(f"[✅] New Brand: {new_brand}")
        print(f"[✅] New Model: {new_model}")

        return True
    except Exception as e:
        print(f"[-] Error changing device profile: {e}")
        return False

def verify_device_profile(expected_manufacturer, expected_brand, expected_model):
    global device
    if not device:
        print("[-] ADB connection failed.")
        return False

    # Get current values
    current_manufacturer = device.shell("getprop ro.product.manufacturer").strip()
    current_brand = device.shell("getprop ro.product.brand").strip()
    current_model = device.shell("getprop ro.product.model").strip()

    print(f"📢 Verifying Device Profile:")
    print(f"    📌 Manufacturer: {current_manufacturer} (Expected: {expected_manufacturer})")
    print(f"    📌 Brand: {current_brand} (Expected: {expected_brand})")
    print(f"    📌 Model: {current_model} (Expected: {expected_model})")

    # Check if values match
    if (current_manufacturer == expected_manufacturer and
        current_brand == expected_brand and
        current_model == expected_model):
        print("[✅] Profile successfully changed!")
        return True
    else:
        print("[-] Profile change failed or reverted.")
        return False

def get_device_profile():
    global device
    if not device:
        print("[-] ADB connection failed.")
        return False

    # Get current values
    current_manufacturer = device.shell("getprop ro.product.manufacturer").strip()
    current_brand = device.shell("getprop ro.product.brand").strip()
    current_model = device.shell("getprop ro.product.model").strip()

    print(f"📢Device Profile:")
    print(f"    📌 Manufacturer: {current_manufacturer})")
    print(f"    📌 Brand: {current_brand} )")
    print(f"    📌 Model: {current_model}")

    
def change_resolution(width=1280, height=720, dpi=240):
    global device
    #device = connect_adb()
    if not device:
        print("[-] ADB connection failed.")
        return False
    try:
        print(f"[+] Setting resolution to {width}x{height} and DPI to {dpi}...")
        device.shell(f"wm size {width}x{height}")  # Change screen size
        device.shell(f"wm density {dpi}")  # Change DPI
        print("[+] Resolution changed successfully!")
        return True
    except Exception as e:
        print(f"[-] Error changing resolution: {e}")
        return False
    

def scroll_up():
    global device
    """ Scroll up (move content down) """
    device.shell("input swipe 500 1500 500 500")

def scroll_down():
    global device
    """ Scroll down (move content up) """
    device.shell("input swipe 500 500 500 1500")

def read_ui():
    global device
    if device is None:
        print("[-][read_ui] Device is not initialized!")
        return False

    try:
        # Dump UI XML
        device.shell("uiautomator dump /sdcard/ui.xml")
    except Exception as e:
        print(f"[-][read_ui] Error Dumping ui.xml file: {e}")
        return False

    try:
        # Pull UI XML to local machine
        device.pull("/sdcard/ui.xml", "ui.xml")
        print("[+] UI XML extracted successfully!")
        return True
    except Exception as e:
        print(f"[-][read_ui] Error Pulling ui.xml file: {e}")
        return False


def click_bounds(bounds):
    global device
    # Extract coordinates using regex
    #device = connect_adb()

    match = re.search(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
    if match:
        x1, y1, x2, y2 = map(int, match.groups())
        x_center = (x1 + x2) // 2  # Find center X
        y_center = (y1 + y2) // 2  # Find center Y
        
        # Tap on the center of the element
        device.shell(f"input tap {x_center} {y_center}")
        print(f"Tapped at: ({x_center}, {y_center})")
    else:
        print("Invalid bounds format!")

def write_text(text):
    global device

    if device :
        device.shell(f'input text {text}')
    else:
        print("Couldn't write text Device not Ready")

def is_google_account_exists():
    global device
    try:
        # Run ADB command to list accounts
        output = device.shell("content query --uri content://accounts/accounts")

        # Check if any Google account is found
        return "com.google" in output  # ✅ True if Google account exists, False otherwise

    except Exception as e:
        print(f"[-] Error checking Google account: {e}")
        return False