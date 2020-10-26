INSTANCES = 405
ITERS     = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
N_ITERS   = len(ITERS)

# === RESULTS GATHERING ====================================================== #
# results_m is a [INSTANCES][N_ITERS] matrix to store every test result
results_m = [[0 for x in range(N_ITERS)] for y in range(INSTANCES)]

for I in range(N_ITERS):
    fin = open("tests/" + str(ITERS[I]))
    out = fin.read()
    fin.close()

    counter = 0
    for line in out.splitlines():
        results_m[counter][I] = int(line)
        counter += 1

# === CALCULATING AVERAGES =================================================== #
averages = [0.0 for x in range(N_ITERS)]

for I in range(INSTANCES):
    for J in range(N_ITERS):
        results_m[I][J] = results_m[I][J] - results_m[I][0]
        if (results_m[I][N_ITERS-1] != 0):
            results_m[I][J] = float(results_m[I][J] / results_m[I][N_ITERS-1])
        averages[J] += results_m[I][J]

for J in range(N_ITERS):
    averages[J] = averages[J]/INSTANCES

for J in range(N_ITERS-1, 1, -1):
    averages[J] -= averages[J-1]

# === PRINTING RESULTS ======================================================= #
print("========================================")
print("incremental improvements by number of iterations:")
for J in range(1, N_ITERS):
    if   (ITERS[J] < 10):
        # print("    " + str(ITERS[J]) + ":     " + str(100 * averages[J]) + '%')
        print("    " + str(ITERS[J]) + ":     " + str(100 * averages[J]) + '%')
    elif (ITERS[J] < 100):
        # print("    " + str(ITERS[J]) + ":    " + str(100 * averages[J]) + '%')
        print("    " + str(ITERS[J]) + ":    " + str(100 * averages[J]) + '%')
    elif (ITERS[J] < 1000):
        # print("    " + str(ITERS[J]) + ":   " + str(100 * averages[J]) + '%')
        print("    " + str(ITERS[J]) + ":   " + str(100 * averages[J]) + '%')
    elif (ITERS[J] < 10000):
        # print("    " + str(ITERS[J]) + ":  " + str(100 * averages[J]) + '%')
        print("    " + str(ITERS[J]) + ":  " + str(100 * averages[J]) + '%')
    else:
        # print("    " + str(ITERS[J]) + ": " + str(100 * averages[J]) + '%')
        print("    " + str(ITERS[J]) + ": " + str(100 * averages[J]) + '%')
print("========================================")
# ============================================================================ #
