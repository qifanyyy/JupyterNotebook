############################################
#
# Jose Marcelo Sandoval-Castaneda (jms1595)
# Artificial Intelligence, Fall 2018
# 01 Nov 2018
#
############################################

import functions

# Load clauses.
clauses = functions.load_clauses('clauses.txt')
# Execute Davis-Putnam.
result = functions.davis_putnam(clauses)
# Write results of Davis-Putnam onto a file.
functions.write_to_file('dp-output.txt', result)
