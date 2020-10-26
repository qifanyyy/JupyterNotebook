############################################
#
# Jose Marcelo Sandoval-Castaneda (jms1595)
# Artificial Intelligence, Fall 2018
# 01 Nov 2018
#
############################################

import copy


# Loads the clauses from the file in a form understandable for davis_putnam.py.
def load_clauses(file_name):
    with open(file_name) as clauses_file:
        clauses = []
        for line in clauses_file:
            # Stops when it finds a 0.
            if line == '0':
                break
            clauses.append(line.strip().split())

    clauses_matrix = []
    for clause in clauses:
        c = []
        for element in clause:
            c.append([abs(int(element)), False if int(element) > 0 else True])
        clauses_matrix.append(c)

    return clauses_matrix


# Loads the output from davis_putnam.py to be printed in a text file.
def load_dp_output(file_name):
    with open(file_name) as output_file:
        output = []
        for line in output_file:
            # Stops when it finds a 0.
            if line == '0':
                break
            output.append(line.strip().split())

    output_list = []
    for line in output:
        if line[1] == 'False':
            b_val = False
        else:
            b_val = True
        output_list.append([line[0], b_val])

    return output_list


# Loads the clauses from the file in a form understandable for front_end.py.
def load_key(file_name):
    with open(file_name) as output_file:
        key = []
        for line in output_file:
            key.append(line.strip().split())

    key_list = []
    for line in key:
        num = line[0]
        name = ''.join(line[1:])
        key_list.append([num, name])

    return key_list


# Called to execute the Davis-Putnam algorithm.
def davis_putnam(clauses):
    atoms = []
    values = {}

    # Make a list of atoms that have already been seen and a dictionary
    # of atoms mapped to their value initiated to None.
    for clause in clauses:
        for atom in clause:
            if atom[0] in atoms:
                continue
            atoms.append(atom[0])
            values[atom[0]] = None

    # Runs the Davis-Putnam algorithm recursively.
    res = dp1(clauses, values)

    # Return '0' if no solution has been found.
    if res is None:
        return '0'

    # Format it to a string.
    res_str = ''
    for a, val in res.items():
        res_str += str(a) + ' ' + str(val) + '\n'

    return res_str + '0'


# Recursive part of the Davis-Putnam algorithm.
def dp1(clauses, values):
    old_values = copy.deepcopy(values)

    # Loop indefinitely.
    while True:
        # If there are no more clauses, a solution has been found.
        if not clauses:
            return values

        # If an empty clause is found, this is not a solution.
        for clause in clauses:
            if not clause:
                return None

        # Find all pure literals in the clauses.
        pure_literals = []
        seen = []
        for clause in clauses:
            for atom in clause:
                if atom[0] in seen:
                    continue
                if [atom[0], not atom[1]] in pure_literals:
                    pure_literals.remove([atom[0], not atom[1]])
                    seen.append(atom[0])
                    continue
                elif [atom[0], atom[1]] in pure_literals:
                    continue
                pure_literals.append(atom)

        # Remove all clauses with pure literals and assign the corresponding truth value.
        for pl in pure_literals:
            values[pl[0]] = not pl[1]
            clauses_copy = copy.deepcopy(clauses)
            for clause in clauses_copy:
                if pl in clause:
                    clauses.remove(clause)

        # Find all singletons in the clauses and remove them.
        for clause in clauses:
            if len(clause) == 1:
                values[clause[0][0]] = not clause[0][1]
                clauses = propagate(clause[0][0], clauses, not clause[0][1])

        # Break if no change has happened since last iteration.
        if old_values == values:
            break
        old_values = copy.deepcopy(values)

    # Find an atom that has not been assigned yet.
    atom = 0
    for a, val in values.items():
        if val is None:
            atom = a
            break

    # If no atom has been found, this is not a solution.
    if atom == 0:
        return None

    # Assign said atom to True and execute on a copy of the clauses and values.
    clauses_1 = copy.deepcopy(clauses)
    values[atom] = True
    clauses_1 = propagate(atom, clauses_1, True)
    values_1 = dp1(clauses_1, copy.deepcopy(values))

    # If a solution has been found, return it.
    if values_1 is not None:
        return values_1

    # If no solution was found, assign atom to False and execute.
    values[atom] = False
    clauses_1 = propagate(atom, clauses, False)

    return dp1(clauses_1, values)


# Propagates an atom with an assigned truth value over the clauses.
def propagate(atom, clauses, value):
    clauses_copy = copy.deepcopy(clauses)
    for clause in clauses:
        if ([atom, False] in clause and value) or ([atom, True] in clause and not value):
            clauses_copy.remove(clause)
        elif [atom, True] in clause and value:
            clauses_copy[clauses_copy.index(clause)].remove([atom, True])
        elif [atom, False] in clause and not value:
            clauses_copy[clauses_copy.index(clause)].remove([atom, False])

    return clauses_copy


# Writes a string s on a file.
def write_to_file(file_name, s):
    with open(file_name, 'w') as f:
        f.write(s)
