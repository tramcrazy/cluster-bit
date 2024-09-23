import microbit

def wait_for_task():
    while True:
        if microbit.uart.any():
            received_text = str(microbit.uart.read(), "utf-8")
            if received_text == "TASKWAITING\n":
                break

def send_code(category):
    if category == 1:
        message = "SENDLINE"
    elif category == 2:
        message = "RUNNINGTASK"
    elif category == 3:
        message = "TASKDONE"
    microbit.uart.write(message + "\n")            

while True:
    wait_for_task()
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
    import taskfile
    results = taskfile.task()
    send_code(3)
    microbit.uart.write(str(results) + "\n")