import pyautogui as pag
import time
import pyperclip
actions = [
    (109, 451, 2),  
    (589, 495, 2), 
    (722, 429, 1),  
    (708, 22, 7),   
    (83, 170, 2),  
    (465, 68, 2),   
    (798, 386, 2),  
    (415, 224, 2),  
    (291, 250, 2),  
    (310, 338, 2),  
    (631, 427, 2),  
    (95, 22, 2),    
    (165, 168, 2),  
    (199, 178, 2),  
    (138, 167, 2),  
    (163, 182 ,2)  
]
time.sleep(2)
for x, y, duration in actions:
    if (x, y) == (165, 168) or (x, y) == (138, 167):
        # For right-click coordinates, perform right-click
        pag.rightClick(x, y, duration=duration)
    else:
        pag.click(x, y, duration=duration)
    if (x, y) in [(291, 250), (310, 338)]:
        pag.keyDown('D')  # Press the "D" key
        text_to_type = "Disalardp1"
        pag.typewrite(text_to_type)

def save_echo_to_batch(file_path, echo_text):
    with open(file_path, 'a') as file:
        file.write(f'\necho {echo_text}\n')

def run_rustdesk_command():
    clipboard_text = pyperclip.paste()
    #password_echo = 'Password : Disalardp1'  
    password_echo = 'Password : Disalardp1'  
    print("Rustdesk ID: " + clipboard_text) 
    print(password_echo)
    #save_echo_to_batch('show.bat', f'RustDesk ID: {clipboard_text}')
    #save_echo_to_batch('show.bat', password_echo)

if __name__ == "__main__":
    run_rustdesk_command()
