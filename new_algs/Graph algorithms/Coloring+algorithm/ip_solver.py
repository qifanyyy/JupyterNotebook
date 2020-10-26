""" Graph coloring MIP solver"""
from itertools import product

from ortools.linear_solver import pywraplp

from .utils import *


class IPSolver:

    def __init__(self, graph):
        self.graph = graph
        self.colors = range(len(graph.vertices))

        self.solver = pywraplp.Solver('VertexColoringMIP',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        self._build_model()

    def _build_model(self):
        # build variables:
        self.vertex_colors_map = {}
        for vertex, color in product(self.graph.vertices, self.colors):
            var_name = 'Vertex{}_Color{}'.format(vertex, color)
            variable = self.solver.IntVar(0, 1, var_name)
            self.vertex_colors_map[var_name] = variable
        self.vertex_colors = self.vertex_colors_map.values()

        self.color_used_map = {}
        for color in self.colors:
            var_name = 'Color{}'.format(color)
            variable = self.solver.IntVar(0, 1, var_name)
            self.color_used_map[var_name] = variable
        self.color_used = self.color_used_map.values()

        # add adjacency constraints
        for color, pair in product(self.colors, self.graph.adjacents()):
            names = ['Vertex{}_Color{}'.format(v, color) for v in pair]
            # for each color, adjacent vertices
            variables = [self.vertex_colors_map[name] for name in names]
            adj_constr = self.solver.Constraint(0, 1)
            adj_constr.SetCoefficient(variables[0], 1)
            adj_constr.SetCoefficient(variables[1], 1)

        # add coloring constraint
        for vertex in self.graph.vertices:
            constr = self.solver.Constraint(1, 1)
            names = ['Vertex{}_Color{}'.format(vertex, color) for color in self.colors]
            variables = [self.vertex_colors_map[name] for name in names]
            for var in variables:
                constr.SetCoefficient(var, 1)

        # color used contraint
        for color in self.colors:
            color_var = self.color_used_map['Color{}'.format(color)]
            names = ['Vertex{}_Color{}'.format(v, color) for v in self.graph.vertices]
            variables = [self.vertex_colors_map[name] for name in names]

            for var in variables:
                constr =  self.solver.Constraint(-self.solver.Infinity(), 0)
                constr.SetCoefficient(color_var, -1)
                constr.SetCoefficient(var, 1)

        # set objective
        objective = self.solver.Objective()
        for var in self.color_used:
            objective.SetCoefficient(var, 1)
        objective.SetMinimization()

    def solve(self):
        result_status = self.solver.Solve()
        assert result_status == pywraplp.Solver.OPTIMAL
        self.nb_variables = self.solver.NumVariables()
        self.nb_constraints = self.solver.NumConstraints()
        self.nb_colors = len([col for col in self.color_used if col])

        lst = []
        for var in self.vertex_colors:
            if var.solution_value():
                vertexID = varname_to_vertexID(var.name())
                colorID = varname_to_colorID(var.name())
                lst.append([vertexID, colorID])
        colors = [pair[1] for pair in lst]
        color_map = normalize_ints(colors)
        for pair in lst:
            pair[1] = color_map[pair[1]]
        return sorted(lst)
