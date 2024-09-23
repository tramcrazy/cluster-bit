def task():
    results_filename = "results.txt"
    times_table = []
    for i in range(1, 13):
        times_table.append(str(i) + " x 2 = " + str(i * 2))
    with open(results_filename, "w") as results:
        for line in times_table:
            results.write(line)
    return results_filename