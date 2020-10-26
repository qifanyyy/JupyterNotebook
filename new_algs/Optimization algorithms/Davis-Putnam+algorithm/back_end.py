############################################
#
# Jose Marcelo Sandoval-Castaneda (jms1595)
# Artificial Intelligence, Fall 2018
# 01 Nov 2018
#
############################################

import functions

# Load the Davis-Putnam output and the key.
dp = functions.load_dp_output('dp-output.txt')
key = functions.load_key('key.txt')

# Assign truth values to the names in the key.
output = []
for d in dp:
    for k in key:
        if d[0] == k[0]:
            output.append([k[1], d[1]])
            break

# Make a list only of the truth values to establish a path and sort it.
ans = []
for i in range(len(output)):
    if output[i][1]:
        ans.append(output[i])
ans.sort(key=lambda x: int(x[0][-1]))

# Write the path onto a string.
output_str = ''
for val in ans:
    output_str += val[0] + '\n'

# Write the string onto a file.
functions.write_to_file('output.txt', output_str)
