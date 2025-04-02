import os
import sys
import time 
import adb_utils as ab
import xmlparser as ui
import blconfig as bl
import proc
import random
import xml.etree.ElementTree as et
import pyautogui as pag

import argparse




PORT = 5555

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, help="Port number")
args = parser.parse_args()
if args.port:
    PORT = args.port
    print(f"Port: {args.port}")
else:
    print("No port provided use default port 5555. ")
    PORT = 5555


FULLSCREN_MENU_X = 836 
FULLSCREN_MENU_Y = 306
FULL_DURATION = 1 


IN_ALLOWED = False 

BLUESTACKS_PATH = r"C:\Program Files\BlueStacks_nxt\HD-Player.exe --instance Tiramisu64"
PACK_PATH       = r"D:\a\master\master\downloads\Haganboy.apk"
WINDOW_TITLE = "BlueStacks App Player"
PACK_NAME = "com.elnimr.haganboy"

HOST = "127.0.0.1"
APP_LOADING_TIME = 10

BS_STARTING_PERIOD = 60
APP_LAUNCING_PERIOD = 20
APP_INSTALLING_PERIOD = 15 
INSTALL_WAIT_PERIOD = 5 
CLICK_PERIOD = 5

APP_STORE = "com.android.vending"
APP_GMS = "com.google.android.gms"
READ_UI_WAIT_TIME = 1
DEBUG = True 


autoSignIn = True 
clear_screen_timer = 0 
dontKnowWhatIamDoingHereTimer = 0 
dontKnowPeriod= 60
EM = "abdoalrahmanm447@gmail.com"



bl.set_adb_access(True) 

#isSignedIn = bl.check_google_account()
bl.changeResolution()

proc.disable_firewall()

proc.start_proc(BLUESTACKS_PATH)
print(f"[+] Waiting {BS_STARTING_PERIOD}s To Start BlueStack")
time.sleep(BS_STARTING_PERIOD)

ab.connect(host=HOST,port=PORT)


while True :

    if clear_screen_timer > 300 :
        os.system('cls')
        clear_screen_timer = 0
        print("[+] Screen Cleared after 300s")

    #proc.move_and_focus_window(WINDOW_TITLE)

    if proc.is_proc_running("HD-Player.exe"): # Main Cycle if the Applicaion is running         
        if ab.is_app_installed(PACK_NAME) : # Check if app installed 
            if ab.is_app_running(PACK_NAME) : # Check if the app is running 
                
                
                '''
                if not isSignedIn and autoSignIn :
                    autoSignIn = False  
                    if DEBUG : print(f"[+] Requesing Sign in With Google Account ...")
                    ab.launch_play_store()
                    time.sleep(5) 
                '''

                if DEBUG : print(f"[+] Reading UI .xml...")

                ab.read_ui()                 
                tree = et.parse("ui.xml")  
                root = tree.getroot()
                current_package = None 
                for node in root.iter("node"):
                    current_package = node.attrib.get("package") 
                    if current_package:  
                        break
                
                   
                if current_package  ==  PACK_NAME : 

                    if DEBUG : print(f"[+] In {PACK_NAME} ...")
                    install = installnow = playnow = play = close = adiframe = agegate = False 
                    install_bound = installnow_bound =  playnow_bound = play_bound = close_bound = agegate_bound =""
                    for node in root.iter("node") :
                        if node.attrib.get("text")  == "Install" : 
                            install  = True 
                            install_bound = node.attrib.get("bounds")
                        if node.attrib.get("text")  == "Install Now" : 
                            installnow  = True
                            installnow_bound = node.attrib.get("bounds")
                        if node.attrib.get("text")  == "Play Now" : 
                            playnow  = True
                            playnow_bound = node.attrib.get("bounds")
                        if node.attrib.get("text")  == "Play" : 
                            play  = True
                            play_bound = node.attrib.get("bounds")
                        if node.attrib.get("text")  == "Close" : 
                            close  = True
                            close_bound = node.attrib.get("bounds")
  
