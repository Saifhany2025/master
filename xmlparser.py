
import xml.etree.ElementTree as ET

def find_element_by_text(text):
    tree = ET.parse("ui.xml")
    root = tree.getroot()
    for node in root.iter("node"):
        if node.attrib.get("text") == text:
            return node.attrib.get("bounds")
    return None


def find_element_by_widget(widget):
    tree = ET.parse("ui.xml")
    root = tree.getroot()
    for node in root.iter("node"):
        if node.attrib.get("class") == widget:
            return node.attrib.get("bounds")
    return None


def find_element(_class,text=""):
    tree = ET.parse("ui.xml")
    root = tree.getroot()
    for node in root.iter("node"):
        if node.attrib.get("class") == _class and node.attrib.get("text") == text:     
            return node.attrib.get("bounds")
    return None


def identify_login_ui():

    tree = ET.parse("ui.xml")    
    root = tree.getroot()
    
    for node in root.iter("node"):

        if node.attrib.get("package") == "com.android.vending":
            
            for node in root.iter("node") :
                if node.attrib.get("text") == "Sign in" :
                    return "signin"
                
                
                if node.attrib.get("text") == "Not now" :
                    return "notnow" 
                                
                a = b = g = False 
                for node in root.iter("node") :
                    if node.attrib.get("text") == "Apps":
                        a = True 
                    if  node.attrib.get("text") == "Games":
                        g = True 
                    if node.attrib.get("text") == "Books":
                        b = True 
                    if a and g and b :
                        return "playstore"
            
        if node.attrib.get("package") == "com.google.android.gms":
            
            uid = pwd = sign = pwd2 = next = welcome = privacyPolicy = iagree = gs = more=  accept = backup = notnow = False 
            for node in root.iter("node") : 

                if node.attrib.get("text")  == "Sign in" : sign  = True                
                if node.attrib.get("text")  == "Welcome" : welcome = True                
                if node.attrib.get("text")  == "Show password" : pwd2 = True 
                if node.attrib.get("text")  == "Google services" : gs = True 
                if node.attrib.get("text")  == "Privacy Policy" : privacyPolicy = True 
                if node.attrib.get("text")  == "Back up device data" : backup = True 
                if node.attrib.get("class") == "android.widget.EditText" and node.attrib.get("password") == "false"   : uid = True 
                if node.attrib.get("class") == "android.widget.EditText" and node.attrib.get("password") == "true"    : pwd = True 
                if node.attrib.get("class") == "android.widget.Button"   and node.attrib.get("text") == "Next" : next = True
                if node.attrib.get("class") == "android.widget.Button"   and node.attrib.get("text") == "I agree" : iagree = True
                if node.attrib.get("class") == "android.widget.Button"   and node.attrib.get("text") == "MORE" : more = True
                if node.attrib.get("class") == "android.widget.Button"   and node.attrib.get("text") == "ACCEPT" : accept = True
                

            if sign and uid and next:
                return "email"
            if pwd and pwd2 and next:
                return "password"
            if privacyPolicy and iagree:
                return "privacy"
            if gs and more and backup  : 
                return "gservices"
            if gs and accept and backup  : 
                return "gservices"
                
            return "mailservice"
        
        return None  


def identify_app_ui():

    tree = ET.parse("ui.xml")    
    root = tree.getroot()
    

    for node in root.iter("node"):
       
        if node.attrib.get("package") == "com.elnimr.haganboy":
            
            install = installnow = close = adframe = playnow = False 

            for node in root.iter("node") :
                if node.attrib.get("class") == "android.widget.Button" and node.attrib.get("text")  == "Install" : install  = True 
                if node.attrib.get("class") == "android.widget.TextView" and node.attrib.get("text")  == "Install" : install  = True 
                if node.attrib.get("class") == "android.widget.Button" and node.attrib.get("text")  == "Install Now" : installnow  = True 
                if node.attrib.get("class") == "android.widget.Button" and node.attrib.get("text")  == "Play Now" : playnow  = True 
                if node.attrib.get("class") == "android.widget.Button" and node.attrib.get("text")  == "Close" : close  = True 
                if node.attrib.get("text")  == "Unity Ads MRAID WebView" : adframe = True 


            if adframe :
                    return "adframe"    
                         
            if installnow == True and  install == False and close == False : 
                return "installnow"
            
            if playnow == True and  install == False and close == True : 
                return "playnowclose"
            
            
            if installnow == True and  install == False and close == True : 
                return "closeinstallnow"
                
            if installnow == False and  install == True and close == True : 
                return "closeinstall"
                
            if installnow == False and  install == False and close == True : 
                return "close"
                
            if installnow == False and  install == True and close == False : 
                return "install"
                      
            return "game"
        
        return None
    
    return False


def identify_Installation():

    tree = ET.parse("ui.xml")    
    root = tree.getroot()

    install = open = cancel = play = uninstall =  installing = False 
    open 
    for node in root.iter("node"):

        if node.attrib.get("package") == "com.android.vending":
            if node.attrib.get("class") == "android.widget.TextView" and node.attrib.get("text")  == "Install" : install  = True
            if node.attrib.get("class") == "android.widget.TextView" and node.attrib.get("text")  == "Cancel" : cancel  = True
            if node.attrib.get("class") == "android.widget.TextView" and node.attrib.get("text")  == "Play" : play  = True
            if node.attrib.get("class") == "android.widget.TextView" and node.attrib.get("text")  == "Open" : open  = True
            if node.attrib.get("class") == "android.widget.TextView" and node.attrib.get("text")  == "Uninstall" : uninstall  = True
            if node.attrib.get("class") == "android.widget.TextView" and node.attrib.get("text")  == "Installing" : installing  = True
    
    if uninstall == True and play == True :
        return "play"
    
    if uninstall == True and open == True :
        return "open"
    
    if install == True :
        return "install"

    if cancel == True and play == True :
        return "installing"
    
    if cancel == True and open == True :
        return "installing"
    
    
     
    