import serial
import serial.tools.list_ports
import sys
import tkinter
from tkinter import filedialog
import time

def autodetect_microbits(): # Searches for micro:bits, returns port if one is found, prints troubleshooting and exits if 0 or >1 micro:bits found
    print("Attempting autodetection of your micro:bit...")
    ports = serial.tools.list_ports.comports() # all serial ports on computer
    microbit_num = 0 # how many micro:bits are connected?
    for port in ports:
        if "VID:PID=0D28:0204" in port.hwid: # checks each port to see if micro:bit vendor/product ID is present
            microbit_port = port.device # stores the micro:bit's port for later
            microbit_name = port.name # store friendlier name for later
            microbit_num += 1
    if microbit_num == 0: # troubleshooting advice when no micro:bit is connected
        print("""It seems like your micro:bit isn't connected to this computer.
Make sure it's connected with a USB data cable and run cluster:bit again.""")
        sys.exit()
    if microbit_num > 1: # troubleshooting advice when more than one micro:bit is connected
        print("""It seems like more than one micro:bit is connected to your computer.
cluster:bit is designed to work with just one micro:bit over USB, and the others over radio.
Try disconnecting any other micro:bits and run cluster:bit again.""")
        sys.exit()
    print("A micro:bit has been detected on port " + microbit_name + ". Let's get clustering!")
    return microbit_port

tkinter_root = tkinter.Tk() # setup Tkinter
tkinter_root.withdraw() # hide root window

print("Welcome to cluster:bit!")
connected_port = autodetect_microbits()

print("""You must select a task file to run on the cluster, which should be in the standard format (https://tramcrazy.com/taskfiles).
A file picker will open soon...""")
time.sleep(4)
taskfile_path = filedialog.askopenfilename()
print(taskfile_path)