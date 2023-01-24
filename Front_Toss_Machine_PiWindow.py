from serial import *
from tkinter import *
import tkinter.font
from PIL import ImageTk, Image
import time

# GUI Window Definition
MainWindow = Tk()
MainWindow.title("Front Toss Machine")
MainWindow.attributes('-fullscreen',True)
#MainWindow.geometry("1080x1920")
myFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

# Serial Definition
ArduinoSerial = Serial("/dev/ttyACM0",9600, timeout=0, writeTimeout=0)
ArduinoSerial.flush()

# Open Main Window Image
rit_logo = Image.open("./Tigers2.png")
# Resize
rit_logo_resized = rit_logo.resize((1500, 915))
# Crop
rit_logo_resized_cropped = rit_logo_resized.crop((300,0,1200,850))
# Add Image to Main Window
img = ImageTk.PhotoImage(rit_logo_resized_cropped)
logo_label = Label(MainWindow, image=img)
logo_label.pack(pady=200)

# Main Window Text
title_label = Label(MainWindow, text="FRONT TOSS MACHINE", font=("Sans 60 bold"))
title_label.pack()
title_label = Label(MainWindow, text="Wait for Baseball Pitch...", font=("FreeSans 50 italic"))
title_label.pack(pady=200)

# Initializing variable for global variable window name
pitchcoming_window = None

# Creating a buffer to read own lines
Buff = ""


# Function that helps read Serial from Arduino
def readSerial():
    while True:
        # Reads the Serial line transmitted, decodes to ASCII, and strips the access spacing 
        c = ArduinoSerial.readline().decode("ASCII").strip()
        
        #Global variable for ready window
        global pitchcoming_window
        
        if len(c) == 0: # If c has nothing in it, break from loop
            break
        
        if  c == "GO": # If c = GO then this means pitch is arriving
            pitchready()
            closingwindow()
            print("c=", c) # Prints the value of c for debugging purposes
            c = ""

        else:
            print("What is in c that is wrong:", c) # Prints the value of c for debugging purposes
            
    MainWindow.after(100, readSerial)


# Function that opens the pitch ready window and adds text labels
def pitchready():
    global pitchcoming_window
    pitchcoming_window = Toplevel()
    pitchcoming_window.attributes('-fullscreen',True)
    #pitchcoming_window.geometry("1080x1920")
    pitchcoming_window.configure(bg='green')
    pitch_label = Label(pitchcoming_window, text="PITCH", font=("Sans 170 bold"), bg=pitchcoming_window['bg'])
    pitch_label.pack(pady=400)
    coming_label = Label(pitchcoming_window, text="COMING", font=("Sans 170 bold"), bg=pitchcoming_window['bg'])
    coming_label.pack()


# Function that closes the pitch ready window
def closingwindow():
    global pitchcoming_window
    pitchcoming_window.after(1000, pitchcoming_window.destroy)


# Function to close main window after "Esc" is pressed
def close_usingesc(e):
    
    MainWindow.destroy()


MainWindow.after(100, readSerial)

# Allows for escape key to be pressed to close window
MainWindow.bind('<Escape>', lambda e: close_usingesc(e))


MainWindow.mainloop() # Loops Forever
