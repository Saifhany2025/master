import subprocess
import psutil
from pywinauto import Application
import pygetwindow as gw
import win32gui
import win32con
import time
import pyautogui


def is_proc_running(proc_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc_name in proc.info['name']:
            return True
    return False


def start_proc(path):
    try:
        subprocess.Popen(path)
        return True 
    except Exception as e:
        print(f"[-] start_proc : {e}")
        return False
    

def Terminate(window_title): 
    try:
        print("process terminating ...")
        app = Application(backend="win32").connect(title=window_title, timeout=10)
        ##pid = app.process
        app.kill()
        print("process terminated ...")
        return True
    except Exception as e:
        print(f"process terminattion faild : {e}") 
        return False


def is_window_open(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    return len(windows) > 0

def move_and_focus_window(window_title):
    """Move the given window to the top-right corner and bring it to the foreground."""
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"[-] No window found with title: {window_title}")
        return False
    
    window = windows[0]
    hwnd = window._hWnd

    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore if minimized
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)  # Ensure it's visible

    # Move window to top-right corner
    screen_width, _ = pyautogui.size()
    window.moveTo(screen_width - window.width, 0)

    time.sleep(0.1)
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print(f"[-] SetForegroundWindow failed: {e}, simulating user interaction...")
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        time.sleep(0.2)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        pyautogui.click(window.left + window.width // 2, window.top + window.height // 2)

    return True


def disable_firewall():
    try:
        result = subprocess.run(
            ["netsh", "advfirewall", "set", "allprofiles", "state", "off"],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            return True
        else:
            print("Error:", result.stderr)
            return False
    except Exception as e:
        print("Exception:", e)
        return False
    
