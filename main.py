from pynput.keyboard import Key, Controller
import time
import os
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog

keyboard = Controller()

def clear_terminal():
    os.system('clear' if os.name == 'posix' else 'cls')

global_timer = None

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def extend_timer(extension):
    global global_timer
    global_timer += extension
    print(f"Timer extended by {extension // 3600} hour(s). New time left: {format_time(global_timer)}")

def show_warning():
    def popup():
        warning_root = tk.Tk()
        warning_root.withdraw()
        
        def add_time(extension):
            warning_root.destroy()
            extend_timer(extension)
        
        warning_window = tk.Toplevel()
        warning_window.title("Warning")
        tk.Label(warning_window, text="Your session will end soon!").pack()
        
        tk.Button(warning_window, text="Extend 1 Hour", command=lambda: add_time(3600)).pack()
        tk.Button(warning_window, text="Extend 3 Hours", command=lambda: add_time(10800)).pack()
        tk.Button(warning_window, text="Extend 5 Hours", command=lambda: add_time(18000)).pack()
        
        warning_window.mainloop()
    
    warning_thread = threading.Thread(target=popup)
    warning_thread.start()

def logout():
    print("Time is up! Logging out...")
    if os.name == 'posix':
        os.system("pkill -KILL -u $USER")
    else:
        os.system("shutdown -l")

def start_timer(duration):
    global global_timer
    global_timer = duration
    while global_timer > 0:
        if global_timer == 10:
            show_warning()
        clear_terminal()
        print(f"Time left: {format_time(global_timer)}")
        time.sleep(1)
        global_timer -= 1
    logout()

root = tk.Tk()
root.withdraw()
timer_duration = simpledialog.askinteger("Input", "Enter logout time in seconds:")
root.destroy()

if timer_duration is None:
    print("No input received. Exiting...")
    exit()

try:
    timer_thread = threading.Thread(target=start_timer, args=(timer_duration,), daemon=True)
    timer_thread.start()
    
    while True:
        keyboard.press(Key.scroll_lock)
        keyboard.release(Key.scroll_lock)
        time.sleep(3)

except KeyboardInterrupt:
    print("Program terminated by user. Exiting...")
