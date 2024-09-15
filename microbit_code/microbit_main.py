import microbit
import utime
def wait_for_task():
    while True:
        if microbit.uart.any():
            received_text = microbit.uart.read()
            if "TASK" in received_text:
                break
        utime.sleep(1)

while True:
    wait_for_task()
    microbit.uart.write("task received!\n")