import microbit
import utime

def wait_for_task():
    while True:
        if microbit.uart.any():
            received_text = str(microbit.uart.read(), "utf-8")
            if "TASKWAITING" in received_text:
                break
        utime.sleep(1)

while True:
    wait_for_task()
    microbit.uart.write("SENDTASK\n")