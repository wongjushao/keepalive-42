from pynput.keyboard import Key, Controller
import time
import os

keyboard = Controller()

def clear_terminal():
    
    os.system('clear' if os.name == 'posix' else 'cls')

try:
    while True:
        
        keyboard.press(Key.scroll_lock)
        keyboard.release(Key.scroll_lock)

        clear_terminal()
        print("running...")
        
        time.sleep(5)

except KeyboardInterrupt:
    print("Program terminated by user. Exiting...")
