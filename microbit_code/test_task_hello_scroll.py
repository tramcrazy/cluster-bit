def task():
    import microbit
    results_filename = "results.txt"
    message = "Hello from cluster:bit!\n"
    microbit.display.scroll(message, wait=True)
    with open(results_filename, "w") as results:
        results.write(message)
    return results_filename