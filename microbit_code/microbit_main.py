import microbit

def send_code(category):
    if category == 1:
        message = "SENDLINE"
    elif category == 2:
        message = "RUNNINGTASK"
    elif category == 3:
        message = "TASKDONE"
    elif category == 7:
        message = "ENDRESULTS"
    microbit.uart.write(message + "\n")            

def write_taskfile():
    send_code(1)
    with open("taskfile.py", "w") as taskfile:
        while True:
            if microbit.uart.any():
                received_text = str(microbit.uart.read(), "utf-8")
                if received_text == "ENDOFTASK\n":
                    send_code(2)
                    break
                taskfile.write(received_text)
                send_code(1)

def wait_for_confirmation(category):
    if category == 1:
        message = "SENDLINE"
    if category == 5:
        message = "TASKWAITING"
    while True:
        if microbit.uart.any():
            received_text = str(microbit.uart.read(), "utf-8")
            if received_text == message + "\n":
                break

def send_results(results_filename):
    with open(results_filename, "rt") as results_file:
        while True:
            line = results_file.readline()
            if len(line) == 0:
                break
            microbit.uart.write(str(line))
            wait_for_confirmation(1)
    send_code(7)

while True:
    wait_for_confirmation(5)
    write_taskfile()
    import taskfile
    results_filename = taskfile.task()
    send_code(3)
    wait_for_confirmation(1)
    send_results(results_filename)