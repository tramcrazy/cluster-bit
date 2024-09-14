def task():
    import microbit
    message = "Hello cluster:bit!"
    microbit.display.scroll(message, wait=True)
    return message