import serial
import serial.tools.list_ports
import sys
import tkinter
from tkinter import filedialog

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
    if category == 1:
        message = "SENDLINE"
    elif category == 2:
        message = "RUNNINGTASK"
    elif category == 3:
        message = "TASKDONE"
    while True:
        received_text = str(serial_connection.readline(), "utf-8")
        if received_text == message + "\n":
            break

def send_code(serial_connection, category):
    if category == 1:
        message = "SENDLINE"
    if category == 5:
        message = "TASKWAITING"
    elif category == 6:
        message = "ENDOFTASK"
    serial_connection.write(message.encode() + b"\n")

def receive_results(serial_connection, results_filename):
    send_code(serial_connection, 1)
    with open(results_filename, "w") as results_file:
        while True:
            received_text = str(serial_connection.readline(), "utf-8")
            if received_text != "":
                if received_text == "ENDRESULTS\n":
                    break
                results_file.write(received_text)
                send_code(serial_connection, 1)

def send_task(serial_connection, task_filename):
    send_code(serial_connection, 5) # notify micro:bit that we have a waiting task
    wait_for_confirmation(serial_connection, 1) # wait for micro:bit to acknowledge
    with open(task_filename, "r") as taskfile: # open the taskfile
        for line in taskfile:
            serial_connection.write(line.encode()) # write one line at a time to serial
            wait_for_confirmation(serial_connection, 1) # wait for confirmation of each line being received
    send_code(serial_connection, 6) # notify micro:bit that we've sent the whole task
    wait_for_confirmation(serial_connection, 2) # wait for micro:bit to acknowledge

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
taskfile_path = filedialog.askopenfilename()
print("Please select where to store the results of the task.\n")
results_filename = filedialog.asksaveasfilename()

print("Sending task to micro:bit...\n")
send_task(serial_connection, taskfile_path)

wait_for_confirmation(serial_connection, 3)
print("Task complete! Saving results...\n")
receive_results(serial_connection, results_filename)

print("Results received and stored in " + results_filename)