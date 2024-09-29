def task():
    results_filename = "results.txt"
    times_table = []
    for i in range(1, 13):
        times_table.append("{} x 2 = {}".format(str(i), str(i*2)))
    with open(results_filename, "wt") as results:
        for line in times_table:
            results.write(line + "\n")
    return results_filename