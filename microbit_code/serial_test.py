from microbit import *
from utime import sleep
uart.init(baudrate=115200)
uart.write("testing serial, hello!\n")
sleep(10)
received = uart.read()
uart.write(str(received, "utf-8") + " RECEIVED SUCCESSFULLY\n")