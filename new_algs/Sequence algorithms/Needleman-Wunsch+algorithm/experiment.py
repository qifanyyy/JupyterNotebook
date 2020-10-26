from alignment import GlobalAlignment
from string_generator import * 
import time

B_RUN_INPUT_TO_LENGTH_10000 = False


string_names_V = ["len 100", "len 100", "len 100", "len 1000", "len 1000", "len 1000", "len 10000", "len 10000", "len 10000"]
string_names_W = ["len 100, mutated", "len 80, substring", "len 80, substring, mutated", "len 1000, mutated", "len 800, substring", "len 800, substring, mutated", "len 10000, mutated", "len 8000, substring", "len 8000, substring, mutated"]
string_arguments_V = [V_100, V_100, V_100, V_1000, V_1000, V_1000, V_10000, V_10000, V_10000]
string_arguments_W = [V_100_P, V_80, V_80_P, V_1000_P, V_800, V_800_P, V_10000_P, V_8000, V_8000_P]
runtimes_NW = [0.0 for i in range(9)]
runtimes_HB = [0.0 for i in range(9)]
memory_usage_NW = [0 for i in range(9)]
memory_usage_HB = [0 for i in range(9)]

end_idx = 6
if B_RUN_INPUT_TO_LENGTH_10000:
    end_idx = 9
for i in range(end_idx):
    v = string_arguments_V[i]
    w = string_arguments_W[i]

    # Timing algorithms
    align_obj = GlobalAlignment(v, w)
    t1 = time.perf_counter()

    memory_usage_HB[i] = align_obj.hirschberg()
    t2 = time.perf_counter()

    memory_usage_NW[i] = align_obj.needleman_wunsch()
    t3 = time.perf_counter()

    runtimes_HB[i] = t2 - t1
    runtimes_NW[i] = t3 - t2

print("String lengths and mutation parameters, for each index of data arrays")
print("V")
print(string_names_V)
print("W")
print(string_names_V)
print("")

print("Memory footprint of Needleman")
print(memory_usage_NW)
print("Memory footprint of Hirschberg")
print(memory_usage_HB)
print("")

print("Time duration of Needleman (seconds)")
print(runtimes_NW)
print("Time duration of Hirschberg (seconds)")
print(runtimes_HB)