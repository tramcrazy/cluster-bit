import microbit

def wait_for_task():
    while True:
        if microbit.uart.any():
            received_text = str(microbit.uart.read(), "utf-8")
            if received_text == "TASKWAITING\n":
                break

while True:
    wait_for_task()
    microbit.uart.write("SENDLINE\n")
    with open("taskfile.py", "w") as taskfile:
        while True:
            if microbit.uart.any():
                received_text = str(microbit.uart.read(), "utf-8")
                if received_text == "ENDOFTASK\n":
                    microbit.uart.write("RUNNINGTASK\n")
                    break
                taskfile.write(received_text)
                microbit.uart.write("SENDLINE\n")
    import taskfile
    results = taskfile.task()