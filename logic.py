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
                        if node.attrib.get("text")  == "Unity Ads MRAID WebView" : adiframe  = True

                        if node.attrib.get("text")  == "button-age-gate-over" : 
                            agegate  = True
                            agegate_bound = node.attrib.get("bounds")
                    
                    if agegate == True :
                        ab.click_bounds(agegate_bound)
                        time.sleep(CLICK_PERIOD)

                    if installnow == True and  install == False and close == False :
                        install = installnow = playnow = play = close = adiframe = False
                        if DEBUG : print(f"[+] Ad Running with Install Now Button ...")
                        if IN_ALLOWED :
                            if DEBUG : print(f"[+] Ad Allowd to INSTALL, installing after {INSTALL_WAIT_PERIOD}s ...")
                            time.sleep( random.choice([3, 10]))
                            ab.click_bounds(installnow_bound)
                            time.sleep(CLICK_PERIOD)
                    
                    elif installnow == True  and  install == False and close == True : 
                        install = installnow = playnow = play = close = adiframe = False
                        if DEBUG : print(f"[+] Ad Running with Install Know and Close Buttons ...") 
                        time.sleep(1)                            
                        ab.click_bounds(close_bound)
                        time.sleep(CLICK_PERIOD)
                    elif installnow == False and  install == True  and close == True :  
                        install = installnow = playnow = play = close = adiframe = False
                        if DEBUG : print(f"[+] Ad Running with Install and Close Buttons ...") 
                        time.sleep(1)                            
                        ab.click_bounds(close_bound)
                        time.sleep(CLICK_PERIOD)
                    elif installnow == False and  install == False and close == True :
                        install = installnow = playnow = play = close = adiframe = False
                        if DEBUG : print(f"[+] Ad Running Close Button ...") 
                        time.sleep(1)                            
                        ab.click_bounds(close_bound)
                        time.sleep(CLICK_PERIOD)
                    elif installnow == False and  install == True  and close == False :
                        install = installnow = playnow = play = close = adiframe = False
                        if DEBUG : print(f"[+] Ad Running Install Button Only ...")  
                        time.sleep(1)                            
                        ab.click_bounds(close_bound)
                        time.sleep(CLICK_PERIOD)
                    elif adiframe :
                        if DEBUG : print(f"[+] Ad IFRame Running ...")
                        time.sleep(1)                            
                        ab.click_bounds(close_bound)
                        time.sleep(CLICK_PERIOD)
                    else:
                        if DEBUG : print(f"[+] No Ads Running ...")
                    

                elif current_package ==  APP_STORE :   

                    if DEBUG : print(f"[+] In {APP_STORE} ...")
                    install = cancel = play = open = uninstall = installing = False 
                    install_bound = cancel_bound = play_bound = open_bound = uninstall_bound = installing_bound = ""
                    accsetup = continu = skip = False 
                    accsetup_bound = continu_bound = skip_bound = "[0,0][0,0]"
                    
                    for node in root.iter("node"):
                        
                        if node.attrib.get("text") == "Sign in":
                            if DEBUG : print(f"[+] Start Signing Process Starts in 5s...")
                            time.sleep(5)
                            ab.click_bounds(node.attrib.get("bounds")) 
                            time.sleep(CLICK_PERIOD)

                        if node.attrib.get("text") == "Not now" :
                            ab.click_bounds(node.attrib.get("bounds")) 
                            time.sleep(CLICK_PERIOD)
                        
                        if node.attrib.get("text")  == "No thanks" :
                            ab.click_bounds(node.attrib.get("bounds")) 
                            time.sleep(CLICK_PERIOD)

                        if node.attrib.get("text")  == "Install" : 
                            install  = True
                            install_bound  = node.attrib.get("bounds")
                        if node.attrib.get("text")  == "Cancel" : 
                            cancel  = True
                            cancel_bound  = node.attrib.get("bounds")
                        if node.attrib.get("text")  == "Play" : 
                            play  = True
                            play_bound  = node.attrib.get("bounds")
                        if node.attrib.get("text")  == "Open" : 
                            open  = True
                            open_bound  = node.attrib.get("bounds")
                        if node.attrib.get("text")  == "Uninstall" : 
                            uninstall  = True
                            uninstall_bound  = node.attrib.get("bounds")
                        if node.attrib.get("text")  == "Installing" : 
                            installing  = True
                            installing_bound  = node.attrib.get("bounds")

                        if node.attrib.get("text")  == "Complete account setup" : 
                            accsetup  = True
                            accsetup_bound  = node.attrib.get("bounds")
                        if node.attrib.get("text")  == "Continue" : 
                            continu  = True
                            continu_bound  = node.attrib.get("bounds")
                        if node.attrib.get("text")  == "Skip" : 
                            skip  = True
                            skip_bound  = node.attrib.get("bounds")
                        
                    #print("accsetup=" , accsetup  ,"continu=" ,continu ,"skip=" , skip )    
                    if  accsetup == True and  continu == True  and skip == False :
                            accsetup = continu = skip = False 
                            if DEBUG : print(f"[+] Handle Account Confirmation ...")  
                            time.sleep(1)                            
                            ab.click_bounds(continu_bound)  
                    elif  accsetup == True and  continu == True  and skip == True :
                            accsetup = continu = skip = False 
                            if DEBUG : print(f"[+] Skip Account Confirmation ...")  
                            time.sleep(1)                            
                            ab.click_bounds(skip_bound)  
                             
                    
                    if install == False and cancel == False and play == True and open == False  and  uninstall == True and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        # uninstall == True and play == True 
                        if DEBUG : print(f"[+] Game Installed Successfuly ...")  
                        '''Play Game'''
                        time.sleep(1)                            
                        ab.click_bounds(play_bound)
                        time.sleep(CLICK_PERIOD)
                        app = ab.get_running_app()
                        if DEBUG : print(f"[+] {app} Installed Successfuly waiting 120s")  
                        time.sleep(120)
                        ab.terminate_app(app)
                        if DEBUG : print(f"[+] APP Terminiated ...") 
                        ab.launch_app(PACK_NAME)                                                   

                    elif install == False and cancel == False and play == False and open == True  and  uninstall == True and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        #uninstall == True and open == True :
                        if DEBUG : print(f"[+] APP Installed Successfuly ...")  
                        '''Play Game'''
                        time.sleep(1)                            
                        ab.click_bounds(open_bound)
                        time.sleep(CLICK_PERIOD)
                        app = ab.get_running_app()
                        if DEBUG : print(f"[+] {app} Installed Successfuly waiting 120s")  
                        time.sleep(120)
                        ab.terminate_app(app)
                        if DEBUG : print(f"[+] APP Terminiated ...")  
                        ab.launch_app(PACK_NAME)
                    
                    if install == True and cancel == False and play == True and open == False  and  uninstall == True and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        # uninstall == True and play == True 
                        if DEBUG : print(f"[+] Game Installed Successfuly ...")  
                        '''Play Game'''
                        time.sleep(1)                            
                        ab.click_bounds(play_bound)
                        time.sleep(CLICK_PERIOD)
                        app = ab.get_running_app()
                        if DEBUG : print(f"[+] {app} Installed Successfuly waiting 120s")  
                        time.sleep(120)
                        ab.terminate_app(app)
                        if DEBUG : print(f"[+] APP Terminiated ...") 
                        ab.launch_app(PACK_NAME)                                                   

                    elif install == True and cancel == False and play == False and open == True  and  uninstall == True and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        #uninstall == True and open == True :
                        if DEBUG : print(f"[+] APP Installed Successfuly ...")  
                        '''Play Game'''
                        time.sleep(1)                            
                        ab.click_bounds(open_bound)
                        time.sleep(CLICK_PERIOD)
                        app = ab.get_running_app()
                        if DEBUG : print(f"[+] {app} Installed Successfuly waiting 120s")  
                        time.sleep(120)
                        ab.terminate_app(app)
                        if DEBUG : print(f"[+] APP Terminiated ...")  
                        ab.launch_app(PACK_NAME)
                    



                    elif install == True and cancel == False and play == False and open == False  and  uninstall == False and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        #install == True
                        randominstll = random.choice([True,False])
                        if randominstll :
                            if DEBUG : print(f"[+] INSTALLING GAME ......")  
                            '''Perform install '''
                            time.sleep(1)                            
                            ab.click_bounds(install_bound)
                            time.sleep(CLICK_PERIOD)
                        else:
                            print("[-] Installing App Skipped Due Randomization ... ")                            
                            time.sleep(1)
                            ab.launch_app(PACK_NAME)
                            
                    elif install == False and cancel == True and play == True and open == False  and  uninstall == False and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        #cancel == True and play == True :
                        ''' Currently Installing  '''
                        if DEBUG : print(f"[+] INSTALLING GAME IN PROGRESS...")  
                    
                    elif install == False and cancel == True and play == False and open == True  and  uninstall == False and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        #cancel == True and open == True :
                        '''Currently Installing"'''
                        if DEBUG : print(f"[+] INSTALLING APP IN PROGRESS...")  
                    
                    elif install == False and cancel == True and play == False and open == False  and  uninstall == False and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        #cancel == True :
                        ''' Currently Installing  '''
                        if DEBUG : print(f"[+] INSTALLING GAME IN PROGRESS...")  
                    
                    elif install == True and cancel == True and play == False and open == False  and  uninstall == False and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        #install True cancel == True :
                        ''' Currently Installing  '''
                        if DEBUG : print(f"[+] INSTALLING GAME IN PROGRESS...")  
                    
                    elif install == False and cancel == False and play == False and open == True  and  uninstall == False and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        #open = True :
                        '''Open Game'''
                        time.sleep(1)                            
                        ab.click_bounds(open_bound)
                        time.sleep(CLICK_PERIOD)
                        app = ab.get_running_app()
                        if DEBUG : print(f"[+] {app} Installed Successfuly waiting 120s")  
                        time.sleep(120)
                        ab.terminate_app(app)
                        if DEBUG : print(f"[+] APP Terminiated ...") 
                        ab.launch_app(PACK_NAME)  

                    elif install == False and cancel == False and play == True and open == False  and  uninstall == False and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        #Play = True :
                        '''Play Game'''
                        time.sleep(1)                            
                        ab.click_bounds(play_bound)
                        time.sleep(CLICK_PERIOD)
                        app = ab.get_running_app()
                        if DEBUG : print(f"[+] {app} Installed Successfuly waiting 120s")  
                        time.sleep(120)
                        ab.terminate_app(app)
                        if DEBUG : print(f"[+] APP Terminiated ...") 
                        ab.launch_app(PACK_NAME)  
                    
                    elif install == True and cancel == False and play == True and open == False  and  uninstall == False and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        #Install == True Play = True :
                        '''Play Game'''
                        time.sleep(1)                            
                        ab.click_bounds(play_bound)
                        time.sleep(CLICK_PERIOD)
                        app = ab.get_running_app()
                        if DEBUG : print(f"[+] {app} Installed Successfuly waiting 120s")  
                        time.sleep(120)
                        ab.terminate_app(app)
                        if DEBUG : print(f"[+] APP Terminiated ...") 
                        ab.launch_app(PACK_NAME) 
                    
                    elif install == True and cancel == False and play == False and open == True  and  uninstall == False and  installing == False :
                        install = cancel = play = open = uninstall = installing = False 
                        #Install == True Open = True :
                        '''Open Game'''
                        time.sleep(1)                            
                        ab.click_bounds(open_bound)
                        time.sleep(CLICK_PERIOD)
                        app = ab.get_running_app()
                        if DEBUG : print(f"[+] {app} Installed Successfuly waiting 120s")  
                        time.sleep(120)
                        ab.terminate_app(app)
                        if DEBUG : print(f"[+] APP Terminiated ...") 
                        ab.launch_app(PACK_NAME) 
                    '''
                    else : 
                        if DEBUG : print(f"[+] I Don't Know What iam doing here, return after {dontKnowPeriod}s ...")                         
                        if dontKnowWhatIamDoingHereTimer > dontKnowPeriod :
                            ab.launch_app(PACK_NAME)
                        dontKnowWhatIamDoingHereTimer += 1
                    '''   
                           
                elif current_package ==  APP_GMS : 
                    if DEBUG : print(f"[+] In {APP_GMS} ...")
                    uid = pwd = sign = pwd2 = next = welcome = privacyPolicy = iagree = gs = more=  accept = backup = notnow = False
                    uid_b = pwd_b = sign_b = pwd2_b = next_b = welcome_b = privacyPolicy_b = iagree_b = gs_b = more_b=  accept_b = backup_b = notnow_b = "[0,0][0,0]"
                    
                    for node in root.iter("node"):
                        if node.attrib.get("text")  == "Sign in" : sign  = True                
                        if node.attrib.get("text")  == "Welcome" : welcome = True                
                        if node.attrib.get("text")  == "Show password" : pwd2 = True 
                        if node.attrib.get("text")  == "Google services" : gs = True 
                        if node.attrib.get("text")  == "Privacy Policy" : privacyPolicy = True 
                        if node.attrib.get("text")  == "Back up device data" : backup = True 
                        if node.attrib.get("class") == "android.widget.EditText" and node.attrib.get("password") == "false"   : 
                            uid = True 
                            uid_b = node.attrib.get("bounds") 
                        if node.attrib.get("class") == "android.widget.EditText" and node.attrib.get("password") == "true"    : 
                            pwd = True 
                            pwd_b = node.attrib.get("bounds") 
                        if node.attrib.get("text")  == "Next" : 
                            next = True
                            next_b = node.attrib.get("bounds") 
                        if node.attrib.get("text")  == "I agree" :
                            iagree = True
                            iagree_b = node.attrib.get("bounds") 
                        if node.attrib.get("text")  == "MORE" : 
                            more = True
                            more_b = node.attrib.get("bounds") 
                        if node.attrib.get("text")  == "ACCEPT" : 
                            accept = True
                            accept_b = node.attrib.get("bounds") 
                    
                    if sign and uid and next: 
                        uid = pwd = sign = pwd2 = next = welcome = privacyPolicy = iagree = gs = more=  accept = backup = notnow = False                       
                        ab.click_bounds(uid_b) 
                        time.sleep(CLICK_PERIOD)
                        ab.write_text(EM)
                        time.sleep(1) 
                        ab.click_bounds(next_b)
                        time.sleep(CLICK_PERIOD)

                    if pwd and pwd2 and next:
                        uid = pwd = sign = pwd2 = next = welcome = privacyPolicy = iagree = gs = more=  accept = backup = notnow = False 
                        ab.click_bounds(pwd_b) 
                        time.sleep(CLICK_PERIOD)
                        ab.write_text("Myoldpassword")
                        time.sleep(1) 
                        ab.click_bounds(next_b)
                        time.sleep(CLICK_PERIOD)

                    if privacyPolicy and iagree:
                        uid = pwd = sign = pwd2 = next = welcome = privacyPolicy = iagree = gs = more=  accept = backup = notnow = False 
                        ab.click_bounds(iagree_b) 
                        time.sleep(CLICK_PERIOD)

                    if DEBUG : print("gs=" ,gs," more=",more," backup=",backup)

                    if gs and more :  
                        uid = pwd = sign = pwd2 = next = welcome = privacyPolicy = iagree = gs = more=  accept = backup = notnow = False          
                        ab.click_bounds(more_b) 
                        time.sleep(1)
                        ab.click_bounds(more_b) 
                        time.sleep(CLICK_PERIOD)
                    
                    if gs and accept:   
                        uid = pwd = sign = pwd2 = next = welcome = privacyPolicy = iagree = gs = more=  accept = backup = notnow = False         
                        ab.click_bounds(accept_b) 
                        time.sleep(1)
                        ab.click_bounds(accept_b) 
                        time.sleep(CLICK_PERIOD)
                else: # unkown place , So lunching the app again
                    if DEBUG : print(f"[+] Unkown Place {PACK_NAME} ...")
                    ab.launch_app(PACK_NAME) 
            else : #Launching the app
                if DEBUG : print(f"[+] Launching {PACK_NAME} with in {APP_LAUNCING_PERIOD}s...")
                ab.launch_app(PACK_NAME)
                time.sleep(APP_LAUNCING_PERIOD)
                #if DEBUG : print(f"[+] CLICK Shortcut window confirmation after {FULL_DURATION}s...")
                #pag.click(FULLSCREN_MENU_X, FULLSCREN_MENU_Y, duration=FULL_DURATION)
        else : # Install The Application
            if DEBUG : print(f"[+] Installing {PACK_NAME} ...")
            ab.install_apk(PACK_PATH,PACK_NAME)
            time.sleep(APP_INSTALLING_PERIOD)
    else: # Restarting The Application
        if DEBUG : print(f"[+] Starting {BLUESTACKS_PATH} ...")
        proc.start_proc(BLUESTACKS_PATH)
        time.sleep(BS_STARTING_PERIOD)
    
    time.sleep(1) 

    clear_screen_timer += 1