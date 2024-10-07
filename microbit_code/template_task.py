def task():
    """
    Your code goes inside this function, which MUST be called task. DO NOT change the name of this function.
    Feel free to add any function definitions, import statements or any other valid MicroPython, as long as everything can happen inside this one function.
    Assume that nothing is imported - including the microbit library. Import everything you need.
    Try to keep your tasks as short as possible - radio bandwidth is limited and we want a nice fast cluster!

    Your function MUST return the filename where results are stored (e.g. results.txt)
    The micro:bit has a completely flat filesystem with no folders
    Make sure to end each line of the file with \n otherwise the file will have no newlines which is probably not what you want
    This is especially important for the last line as part of the sending logic depends on knowing we've hit the end of the line
    """
    return "results.txt"