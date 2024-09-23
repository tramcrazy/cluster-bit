import serial
import serial.tools.list_ports
import sys
import tkinter
from tkinter import filedialog
import time

def autodetect_microbits(): # Searches for micro:bits, returns port if one is found, prints troubleshooting and exits if 0 or >1 micro:bits found
    print("Attempting autodetection of your micro:bit...\n")
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
    print("A micro:bit has been detected on port " + microbit_name + ". Let's get clustering!\n")
    return microbit_port

def wait_for_confirmation(serial_connection, category):
    while True:
        if category == 1:
            message = "SENDLINE"
        elif category == 2:
            message = "RUNNINGTASK"
        elif category == 3:
            message = "TASKDONE"
        received_text = str(serial_connection.readline(), "utf-8")
        if received_text == message + "\n":
            break
        time.sleep(0.5)

tkinter_root = tkinter.Tk() # setup Tkinter
tkinter_root.withdraw() # hide root window

print("""Welcome to cluster:bit!
Please ensure your USB-connected micro:bit is running the cluster:bit MicroPython software, found in ./microbit_code/microbit_main.py
If not, exit now and install the software on your micro:bit.\n""")

input("Press enter to confirm your micro:bit is running cluster:bit...\n")

connected_port = autodetect_microbits()
serial_connection = serial.Serial(connected_port, 115200)

print("""You must select a task file to run on cluster:bit, which should be in the standard format (https://tramcrazy.com/taskfiles).
A file picker will open soon...\n""")
time.sleep(4)
taskfile_path = filedialog.askopenfilename()

print("Notifying micro:bit of task...\n")
serial_connection.write(b"TASKWAITING\n") # notify micro:bit that we have a waiting task
wait_for_confirmation(serial_connection, 1) # wait for micro:bit to acknowledge

print("Sending task to micro:bit...\n")
with open(taskfile_path, "r") as taskfile: # open the taskfile
    for line in taskfile:
        serial_connection.write(line.encode()) # write one line at a time to serial
        wait_for_confirmation(serial_connection, 1) # wait for confirmation of each line being received

serial_connection.write(b"ENDOFTASK\n") # notify micro:bit that we've sent the whole task
wait_for_confirmation(serial_connection, 2) # wait for micro:bit to acknowledge
print("Task sent. Awaiting results...")

wait_for_confirmation(serial_connection, 3)
while True:
    received_text = str(serial_connection.readline(), "utf-8")
    if received_text != "":
        break
    time.sleep(0.5)
print("Results received. Printing results...\n")
print(received_text)