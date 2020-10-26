# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 19:39:06 2014

@author: Eugene Petkevich
"""

class VariableFactory(object):

    """A class for a SAT maker that number variables.

    It keeps track of variable numbers
    """

    def __init__(self):
        """Create a factory for a SAT-input."""
        self.count = 0
        self.variables = []

    def next(self):
        """Create and return a new variable."""
        variable = {}
        self.count += 1
        variable["number"] = self.count
        self.variables.append(variable)
        return variable

class ConstraintCollector(object):

    """A class for a SAT maker that collects constraints.

    It stores all constraints.
    """

    def __init__(self):
        """Create a constraint collector."""
        self.constraints = []
        self.xor_constraints = []
        self.literals_count = 0

    def add(self, positive, negative):
        """Add constraint.

        Arguments:
        positive: a list of non-negated variables;
        negative: a list of negated variables.
        """
        constraint = {}
        constraint["positive"] = positive
        constraint["negative"] = negative
        self.constraints.append(constraint)
        self.literals_count = self.literals_count + len(positive) + len(negative)

    def add_xor(self, positive, negative):
        """Add xor constraint.

        Arguments:
        positive: a list of non-negated variables;
        negative: a list of negated variables.
        """
        constraint = {}
        constraint["positive"] = positive
        constraint["negative"] = negative
        self.xor_constraints.append(constraint)
        self.literals_count = self.literals_count + len(positive) + len(negative)


class SatPrinter(object):

    """A class for printing SAT input."""

    def __init__(self, vf, cc):
        """Create a SAT printer.

        Arguments:
        vf: a variable factory;
        cc: a constraints collector.
        """
        self.vf = vf
        self.cc = cc

    def print_statistics(self):
        """Print problem statistics."""
        print('Variables: ' + str(self.vf.count))
        print('Clauses: ' + str(len(self.cc.constraints)))
        print('Xor Clauses: ' + str(len(self.cc.xor_constraints)))
        print('Literals: ' + str(self.cc.literals_count))

    def print(self, file):
        """Print SAT input into a file object in dimacs format."""
        file.write('p cnf ' +
                   str(self.vf.count) + ' ' +
                   str(len(self.cc.constraints) + len(self.cc.xor_constraints)) + '\n')
        for constraint in self.cc.constraints:
            for variable in constraint['positive']:
                file.write(str(variable["number"]) + ' ')
            for variable in constraint['negative']:
                file.write('-' + str(variable["number"]) + ' ')
            file.write('0 \n')
        for constraint in self.cc.xor_constraints:
            file.write('x')
            for variable in constraint['positive']:
                file.write(str(variable["number"]) + ' ')
            for variable in constraint['negative']:
                file.write('-' + str(variable["number"]) + ' ')
            file.write('0 \n')

    def decode_output(self, file):
        """Assign values to variables from a SAT solver output."""
        for line in file:
            if line[0] == 'v':
                values = line[1:].split()
                for v in values:
                    variable_number = int(v)
                    if variable_number != 0:
                        self.vf.variables[abs(variable_number)-1]['value'] = variable_number > 0
