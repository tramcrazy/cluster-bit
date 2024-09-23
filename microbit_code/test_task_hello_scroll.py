def task():
    import microbit
    message = "Hello from cluster:bit!"
    microbit.display.scroll(message, wait=True)
    return message